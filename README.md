# Campus Lost & Found Board

A responsive campus noticeboard for reporting lost/found items with photos, filtering active listings, and archiving claimed items.

## Requirements
- Node.js 18+
- npm
- MongoDB running locally (default: `mongodb://127.0.0.1:27017/campus_lost_found`)

## Configuration

Create a `.env` file in the project root (already included for local use):

```env
PORT=3000
MONGO_URI=mongodb://127.0.0.1:27017/campus_lost_found
```

## Run locally

```bash
npm install
npm start
```

Open http://localhost:3000.

## Features
- Post a Lost or Found listing with title, description, category, location, optional contact, and optional photo.
- Image uploads are accepted as JPG, PNG, WEBP, or GIF up to 5 MB.
- Multer receives the upload in a memory buffer; Node's `fs` module saves the image in `uploads/`.
- Listings are stored in MongoDB via Mongoose (`Item` model).
- Search by free-text query, category, and location using URL query strings.
- Mark a listing claimed/returned; it is archived and shown under **View archived**.
- Responsive browser UI with basic output escaping.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/items?q=...&category=...&location=...&status=active` | Search active listings |
| GET | `/api/items?status=archived` | Search archived listings |
| POST | `/api/items` | Create listing (`multipart/form-data`, field name `photo`) |
| PATCH | `/api/items/:id/claim` | Archive a claimed/returned item |

Example upload fields: `title`, `description`, `category`, `location`, `type` (`Lost` or `Found`), optional `contact`, and optional `photo`.

## Project structure

```text
campus-lost-found/
├── public/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── uploads/       # uploaded photos
├── .env           # PORT and MONGO_URI
├── package.json
└── server.js
```

## Notes before production
This is a classroom/demo app. For a real campus deployment, add authentication and role-based moderation, rate limiting, CSRF protection where applicable, database backups, image re-encoding/scanning, and a private contact workflow. Do not expose personal contact details publicly unless users knowingly consent.
