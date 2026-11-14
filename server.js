
require("dotenv").config();

const express = require("express");
const mongoose = require("mongoose");
const multer = require("multer");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const app = express();
const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/campus_lost_found";

const UPLOAD_DIR = path.join(__dirname, "uploads");

fs.mkdirSync(UPLOAD_DIR, { recursive: true });

function escapeRegex(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));
app.use("/uploads", express.static(UPLOAD_DIR));

// 1. MongoDB Schema
const itemSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true,
        trim: true
    },
    description: {
        type: String,
        required: true,
        trim: true
    },
    category: {
        type: String,
        required: true
    },
    location: {
        type: String,
        required: true,
        trim: true
    },
    type: {
        type: String,
        enum: ["Lost", "Found"],
        required: true
    },
    contact: {
        type: String,
        default: ""
    },
    photoUrl: {
        type: String,
        default: null
    },
    archived: {
        type: Boolean,
        default: false
    },
    createdAt: {
        type: Date,
        default: Date.now
    },
    claimedAt: {
        type: Date,
        default: null
    }
}, {
    toJSON: { virtuals: true },
    toObject: { virtuals: true }
});

// 2. Create MongoDB Model
const Item = mongoose.model("Item", itemSchema);

// 3. Image Upload Configuration
const allowedTypes = new Set([
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif"
]);

const storage = multer.memoryStorage();

const upload = multer({
    storage,
    limits: {
        fileSize: 5 * 1024 * 1024
    },
    fileFilter: (req, file, cb) => {
        if (!allowedTypes.has(file.mimetype)) {
            return cb(new Error("Use JPG, PNG, WEBP or GIF."));
        }
        cb(null, true);
    }
});

// 4. GET - Search and Display Items
app.get("/api/items", async (req, res) => {
    try {
        const {
            q = "",
            category = "",
            location = "",
            status = "active"
        } = req.query;

        const filter = {};

        if (status === "active") {
            filter.archived = false;
        } else if (status === "archived") {
            filter.archived = true;
        }

        if (category.trim()) {
            filter.category = category.trim();
        }

        if (location.trim()) {
            filter.location = {
                $regex: escapeRegex(location.trim()),
                $options: "i"
            };
        }

        if (q.trim()) {
            const searchRegex = {
                $regex: escapeRegex(q.trim()),
                $options: "i"
            };

            filter.$or = [
                { title: searchRegex },
                { description: searchRegex },
                { location: searchRegex },
                { category: searchRegex }
            ];
        }

        const items = await Item.find(filter)
            .sort({ createdAt: -1 });

        res.json(items);

    } catch (error) {
        res.status(500).json({
            error: error.message
        });
    }
});

// 5. POST - Create New Item
app.post("/api/items", upload.single("photo"), async (req, res) => {
    let uploadedFilePath = null;

    try {
        const {
            title,
            description,
            category,
            location,
            type,
            contact
        } = req.body || {};

        if (
            !title?.trim() ||
            !description?.trim() ||
            !category?.trim() ||
            !location?.trim() ||
            !type
        ) {
            return res.status(400).json({
                error: "Please complete all required fields."
            });
        }

        if (!["Lost", "Found"].includes(type)) {
            return res.status(400).json({
                error: "Type must be Lost or Found."
            });
        }

        let photoUrl = null;

        if (req.file) {
            const extensions = {
                "image/jpeg": ".jpg",
                "image/png": ".png",
                "image/webp": ".webp",
                "image/gif": ".gif"
            };

            const filename =
                `${crypto.randomUUID()}${extensions[req.file.mimetype]}`;

            uploadedFilePath = path.join(UPLOAD_DIR, filename);
            fs.writeFileSync(uploadedFilePath, req.file.buffer);

            photoUrl = `/uploads/${filename}`;
        }

        const item = await Item.create({
            title: title.trim(),
            description: description.trim(),
            category: category.trim(),
            location: location.trim(),
            type,
            contact: (contact || "").trim(),
            photoUrl
        });

        res.status(201).json(item);

    } catch (error) {
        if (uploadedFilePath && fs.existsSync(uploadedFilePath)) {
            fs.unlinkSync(uploadedFilePath);
        }

        res.status(500).json({
            error: error.message
        });
    }
});

// 6. PATCH - Mark Item as Claimed
app.patch("/api/items/:id/claim", async (req, res) => {
    try {
        if (!mongoose.isValidObjectId(req.params.id)) {
            return res.status(400).json({
                error: "Invalid item ID."
            });
        }

        const item = await Item.findById(req.params.id);

        if (!item) {
            return res.status(404).json({
                error: "Item not found."
            });
        }

        item.archived = true;
        item.claimedAt = new Date();

        await item.save();

        res.json(item);

    } catch (error) {
        res.status(500).json({
            error: "Could not update listing."
        });
    }
});

// 7. Error Handler
app.use((err, req, res, next) => {
    if (err instanceof multer.MulterError && err.code === "LIMIT_FILE_SIZE") {
        return res.status(400).json({
            error: "Photo must be 5 MB or smaller."
        });
    }

    res.status(400).json({
        error: err.message || "Request could not be processed."
    });
});

// 8. Connect MongoDB and Start Server
async function startServer() {
    try {
        await mongoose.connect(MONGO_URI);

        console.log("MongoDB Connected Successfully!");
        console.log("Database:", mongoose.connection.name);

        const server = app.listen(PORT, () => {
            console.log(`Server running at http://localhost:${PORT}`);
        });

        server.on("error", (error) => {
            if (error.code === "EADDRINUSE") {
                console.error(`Port ${PORT} is already in use. Stop the existing server or change PORT in .env.`);
            } else {
                console.error("Server error:", error.message);
            }
            process.exit(1);
        });

    } catch (error) {
        console.error("MongoDB Connection Failed:", error.message);
        process.exit(1);
    }
}

startServer();
