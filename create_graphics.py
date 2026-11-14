import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

os.makedirs('assets', exist_ok=True)

# Common color palette
C_NAVY_BG = '#0A192F'
C_CARD_BG = '#112240'
C_CARD_BORDER = '#1E3A66'
C_INNER_BG = '#172A4D'
C_CYAN = '#00E5FF'
C_CYAN_LIGHT = '#64FFDA'
C_GREEN = '#10B981'
C_CORAL = '#FF6B6B'
C_SLATE = '#94A3B8'
C_WHITE = '#FFFFFF'
C_GOLD = '#F59E0B'
C_MUTED = '#CBD5E1'

def setup_canvas(width_in, height_in, dpi=120):
    fig = plt.figure(figsize=(width_in, height_in), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_NAVY_BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    return fig, ax

def add_card(ax, x, y, w, h, bg=C_CARD_BG, border=C_CARD_BORDER, lw=1.5, radius=2):
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=bg, edgecolor=border, linewidth=lw
    )
    ax.add_patch(rect)
    return rect

# ==========================================
# GRAPHIC 1: SLIDE 1 HERO VISUAL
# ==========================================
def generate_graphic_1():
    fig, ax = setup_canvas(10, 5.5, dpi=140)
    
    # Outer container
    add_card(ax, 2, 2, 96, 96, bg='#0D1E3A', border=C_CYAN, lw=1.8, radius=3)
    
    # Header badge
    ax.text(50, 91, "CAMPUS COMMUNITY RECOVERY NETWORK", color=C_CYAN,
            fontsize=12, fontweight='bold', ha='center', va='center', fontfamily='sans-serif')
    
    # Central Radar / Scanning Hub
    circle_outer = patches.Circle((50, 50), 22, facecolor='#10284C', edgecolor=C_CYAN, linewidth=2, linestyle='--')
    circle_mid = patches.Circle((50, 50), 15, facecolor='#13325E', edgecolor=C_CYAN_LIGHT, linewidth=1.5)
    circle_inner = patches.Circle((50, 50), 8, facecolor='#1B427A', edgecolor=C_WHITE, linewidth=2)
    ax.add_patch(circle_outer)
    ax.add_patch(circle_mid)
    ax.add_patch(circle_inner)
    
    # Magnifying lens symbol & text
    circle_lens = patches.Circle((50, 52), 4, facecolor='none', edgecolor=C_CYAN, linewidth=2)
    ax.add_patch(circle_lens)
    ax.plot([52.8, 55.5], [49.2, 46.5], color=C_CYAN, linewidth=2.5)
    ax.text(50, 43, "CENTRAL HUB", color=C_WHITE, fontsize=8, ha='center', va='center', fontweight='bold')
    
    # 4 Orbiting Item Nodes with info boxes
    nodes = [
        (20, 72, "STUDENT ID CARD", "Found: Campus Library", C_GREEN, "FOUND"),
        (80, 72, "ELECTRONICS / LAPTOP", "Lost: Science Lab 3", C_CORAL, "LOST"),
        (18, 28, "WATER BOTTLE", "Found: Main Quad", C_GREEN, "FOUND"),
        (82, 28, "KEYS & FOB BUNDLE", "Lost: Lecture Hall B", C_CORAL, "LOST")
    ]
    
    for nx, ny, title, sub, col, tag in nodes:
        # Connecting line to center
        ax.plot([nx, 50], [ny, 50], color='#1E457A', linestyle=':', linewidth=1.5, zorder=1)
        # Node box
        add_card(ax, nx-14, ny-9, 28, 18, bg=C_CARD_BG, border=col, lw=1.6, radius=2)
        # Tag badge
        tag_bg = '#064E3B' if tag == 'FOUND' else '#7F1D1D'
        add_card(ax, nx-12, ny+3.5, 9, 4, bg=tag_bg, border=col, lw=1, radius=1)
        ax.text(nx-7.5, ny+5.5, tag, color=C_WHITE, fontsize=7, fontweight='bold', ha='center', va='center')
        ax.text(nx, ny, title, color=C_WHITE, fontsize=8.5, fontweight='bold', ha='center', va='center')
        ax.text(nx, ny-5, sub, color=C_MUTED, fontsize=7, ha='center', va='center')
    
    # Bottom summary ribbon
    add_card(ax, 15, 6, 70, 7.5, bg='#0B1528', border=C_CARD_BORDER, lw=1, radius=1.5)
    ax.text(50, 9.8, "Connecting Lost Belongs with Rightful Owners Across Campus Buildings",
            color=C_CYAN_LIGHT, fontsize=8.5, ha='center', va='center', fontweight='bold')
    
    fig.savefig('assets/slide1_hero.png', bbox_inches='tight', pad_inches=0.05, facecolor=C_NAVY_BG)
    plt.close(fig)
    print("Graphic 1 saved")

# ==========================================
# GRAPHIC 2: SLIDE 2 DASHBOARD MOCKUP
# ==========================================
def generate_graphic_2():
    fig, ax = setup_canvas(10, 5.8, dpi=140)
    
    # Outer browser window frame
    add_card(ax, 2, 2, 96, 96, bg='#0D192E', border=C_CYAN, lw=2, radius=2.5)
    
    # Browser chrome bar
    add_card(ax, 2, 91, 96, 7, bg='#172A45', border=C_CARD_BORDER, lw=1, radius=0)
    # Window buttons
    for i, col in enumerate(['#FF5F56', '#FFBD2E', '#27C93F']):
        c = patches.Circle((5 + i*2.2, 94.5), 0.9, facecolor=col, edgecolor='none')
        ax.add_patch(c)
    # URL bar
    add_card(ax, 16, 92.2, 68, 4.6, bg='#0A1322', border=C_CARD_BORDER, lw=0.8, radius=1)
    ax.text(50, 94.5, "https://campus-lost-found.edu/board", color=C_MUTED, fontsize=7.5, ha='center', va='center')
    
    # Application Topbar inside browser
    add_card(ax, 4, 82.5, 92, 7.5, bg='#10223D', border=C_CARD_BORDER, lw=1, radius=1.5)
    circle_brand = patches.Circle((7, 86.2), 2.2, facecolor=C_CYAN, edgecolor='none')
    ax.add_patch(circle_brand)
    ax.text(7, 86.2, "Q", color='#0A192F', fontsize=9, fontweight='bold', ha='center', va='center')
    ax.text(11, 87.2, "Campus Lost & Found Board", color=C_WHITE, fontsize=9.5, fontweight='bold', va='center')
    ax.text(11, 84.5, "Find it. Return it. Keep campus connected.", color=C_SLATE, fontsize=6.5, va='center')
    # Post item button
    add_card(ax, 78, 83.8, 16, 5, bg=C_CYAN, border=C_CYAN, lw=1, radius=1)
    ax.text(86, 86.3, "+ Post An Item", color='#0A192F', fontsize=7.5, fontweight='bold', ha='center', va='center')
    
    # Search & Filter Controls Bar
    add_card(ax, 4, 73, 92, 8, bg='#0A192F', border=C_CARD_BORDER, lw=1, radius=1.5)
    # Search Box
    add_card(ax, 6, 74.2, 42, 5.6, bg='#142744', border=C_CYAN, lw=1, radius=1)
    ax.text(8.5, 77, "SEARCH: water bottle, library, keys...", color=C_WHITE, fontsize=7, va='center')
    # Category dropdown
    add_card(ax, 50, 74.2, 19, 5.6, bg='#142744', border=C_CARD_BORDER, lw=1, radius=1)
    ax.text(59.5, 77, "Category: All [v]", color=C_MUTED, fontsize=7, ha='center', va='center')
    # Location input
    add_card(ax, 70.5, 74.2, 14, 5.6, bg='#142744', border=C_CARD_BORDER, lw=1, radius=1)
    ax.text(77.5, 77, "Location [v]", color=C_MUTED, fontsize=7, ha='center', va='center')
    # View Archived button
    add_card(ax, 85.5, 74.2, 9.5, 5.6, bg='#1E3A66', border=C_CYAN_LIGHT, lw=1, radius=1)
    ax.text(90.25, 77, "Archived ->", color=C_CYAN_LIGHT, fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Noticeboard Metadata Subheader
    ax.text(6, 69.5, "ACTIVE COMMUNITY LISTINGS (2 ITEMS DISPLAYED)", color=C_CYAN, fontsize=7, fontweight='bold')
    ax.text(94, 69.5, "SHOWING: ACTIVE ITEMS", color=C_SLATE, fontsize=6.5, ha='right')
    
    # 3 Realistic Sample Item Cards
    cards_data = [
        # (x, tag, tag_color, cat, title, desc, loc, date, contact, btn_text, is_archived)
        (4, "FOUND", C_GREEN, "ACCESSORIES", "Blue Stainless Water Bottle",
         "Blue insulated bottle found on classroom 204 desk.", "Classroom 204", "10/11/2026", "None",
         "Mark as claimed / returned ✓", False),
        (35.5, "LOST", C_CORAL, "KEYS & CARDS", "College Student ID Card",
         "ID card lost near college central library entrance.", "Library, 2nd Fl", "10/11/2026", "9876543210",
         "Mark as claimed / returned ✓", False),
        (67, "CLAIMED", C_SLATE, "ELECTRONICS", "Scientific Calculator",
         "Casio fx-991ES claimed and returned to student.", "Lab 3 Handover", "10/11/2026", "Resolved",
         "Archived Listing (Claimed)", True)
    ]
    
    for cx, tag, tag_col, cat, title, desc, loc, date, cont, btn, archived in cards_data:
        card_border = C_SLATE if archived else (C_CYAN if tag == 'LOST' else C_GREEN)
        card_bg = '#0E1D33' if not archived else '#081220'
        add_card(ax, cx, 5, 29, 62, bg=card_bg, border=card_border, lw=1.6 if not archived else 1, radius=2)
        
        # Photo placeholder box
        photo_bg = '#142744' if not archived else '#0D192C'
        add_card(ax, cx+1.5, 42, 26, 23, bg=photo_bg, border=C_CARD_BORDER, lw=0.8, radius=1.5)
        # Photo icon / label
        photo_label = "[PHOTO] Water Bottle" if "Bottle" in title else ("[PHOTO] Student ID" if "ID" in title else "[CLAIMED] Returned")
        ax.text(cx+14.5, 53.5, photo_label, color=C_CYAN_LIGHT if not archived else C_SLATE,
                fontsize=7.5, fontweight='bold', ha='center', va='center')
        
        # Tags row
        tag_bg = '#064E3B' if tag == 'FOUND' else ('#7F1D1D' if tag == 'LOST' else '#334155')
        add_card(ax, cx+1.5, 36.5, 8.5, 4, bg=tag_bg, border=tag_col, lw=1, radius=1)
        ax.text(cx+5.75, 38.5, tag, color=C_WHITE, fontsize=6.5, fontweight='bold', ha='center', va='center')
        
        add_card(ax, cx+11, 36.5, 12, 4, bg='#1E293B', border=C_CARD_BORDER, lw=0.8, radius=1)
        ax.text(cx+17, 38.5, cat, color=C_MUTED, fontsize=6, ha='center', va='center')
        
        # Title & Description
        ax.text(cx+1.5, 33, title, color=C_WHITE if not archived else C_SLATE, fontsize=8, fontweight='bold')
        ax.text(cx+1.5, 27.5, desc, color=C_MUTED if not archived else '#64748B', fontsize=6.5)
        
        # Location & Date
        ax.plot([cx+1.5, cx+27.5], [23, 23], color=C_CARD_BORDER, linewidth=0.8)
        ax.text(cx+1.5, 19.5, f"LOC: {loc} | {date}", color=C_CYAN_LIGHT if not archived else '#64748B', fontsize=6.5)
        if cont != "None" and cont != "Resolved":
            ax.text(cx+1.5, 15.5, f"Contact: {cont}", color=C_MUTED, fontsize=6.5)
        elif archived:
            ax.text(cx+1.5, 15.5, "Status: Item verified & returned", color=C_GREEN, fontsize=6.5)
            
        # Action button
        btn_bg = C_CYAN if not archived else '#1E293B'
        btn_col = '#0A192F' if not archived else C_SLATE
        add_card(ax, cx+1.5, 7.5, 26, 5.5, bg=btn_bg, border=btn_bg, lw=1, radius=1)
        ax.text(cx+14.5, 10.25, btn, color=btn_col, fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    fig.savefig('assets/slide2_ui_mockup.png', bbox_inches='tight', pad_inches=0.05, facecolor=C_NAVY_BG)
    plt.close(fig)
    print("Graphic 2 saved")

# ==========================================
# GRAPHIC 3: SLIDE 3 ARCHITECTURE
# ==========================================
def generate_graphic_3():
    fig, ax = setup_canvas(10, 5.5, dpi=140)
    
    add_card(ax, 2, 2, 96, 96, bg='#0D192E', border=C_CYAN, lw=1.8, radius=3)
    
    # Left Section: System Architecture (width 54)
    add_card(ax, 4, 5, 52, 90, bg=C_CARD_BG, border=C_CARD_BORDER, lw=1.4, radius=2.5)
    ax.text(30, 91, "FULL-STACK SYSTEM ARCHITECTURE", color=C_CYAN, fontsize=10, fontweight='bold', ha='center')
    
    arch_steps = [
        ("USER / WEB BROWSER", "Desktop, Tablet, or Smartphone Client UI", C_CYAN, 79),
        ("FRONTEND LAYER", "Semantic HTML5 + CSS3 + Vanilla JavaScript (Fetch API)", C_CYAN_LIGHT, 65),
        ("EXPRESS.JS REST API", "REST Endpoints, JSON Routing, Static /uploads/ Hosting", '#38BDF8', 51),
        ("NODE.JS RUNTIME", "Node 18+ Asynchronous Non-Blocking Event-Driven Engine", C_GREEN, 37),
        ("MONGOOSE OBJECT MODEL", "Mongoose Schema, Type Casting, Validations & Queries", C_GOLD, 23),
        ("MONGODB DATABASE", "campus_lost_found (Database) → items (Collection)", C_CORAL, 9)
    ]
    
    for title, desc, col, y in arch_steps:
        add_card(ax, 7, y, 46, 10, bg='#142744', border=col, lw=1.4, radius=1.5)
        ax.text(30, y+6.5, title, color=col, fontsize=8, fontweight='bold', ha='center')
        ax.text(30, y+2.5, desc, color=C_MUTED, fontsize=6.5, ha='center')
        if y > 15:
            ax.annotate("", xy=(30, y-3.5), xytext=(30, y),
                        arrowprops=dict(arrowstyle="->", color=C_WHITE, lw=1.5))
            
    # Right Section: Multipart Image Upload Flow (width 38)
    add_card(ax, 58, 5, 38, 90, bg=C_CARD_BG, border=C_CARD_BORDER, lw=1.4, radius=2.5)
    ax.text(77, 91, "IMAGE UPLOAD PIPELINE", color=C_CYAN, fontsize=10, fontweight='bold', ha='center')
    
    upload_steps = [
        ("1. USER SELECTS PHOTO", "JPG, PNG, WEBP, GIF (Max 5 MB)", 78),
        ("2. MULTIPART SUBMISSION", "FormData payload: name='photo'", 64),
        ("3. MULTER MEMORY STORAGE", "Memory buffer stream & MIME validation", 50),
        ("4. CRYPTO UUID FILENAME", "crypto.randomUUID() + extension", 36),
        ("5. NODE.JS FS MODULE", "fs.writeFileSync() writes to disk", 22),
        ("6. UPLOADS/ DIRECTORY", "/uploads/<uuid>.ext served statically", 8)
    ]
    
    for title, desc, y in upload_steps:
        add_card(ax, 60.5, y, 33, 10, bg='#172D4D', border=C_CYAN_LIGHT, lw=1.2, radius=1.5)
        ax.text(77, y+6.2, title, color=C_WHITE, fontsize=7.5, fontweight='bold', ha='center')
        ax.text(77, y+2.4, desc, color=C_CYAN_LIGHT, fontsize=6.2, ha='center')
        if y > 15:
            ax.annotate("", xy=(77, y-3.5), xytext=(77, y),
                        arrowprops=dict(arrowstyle="->", color=C_CYAN, lw=1.3))
            
    fig.savefig('assets/slide3_architecture.png', bbox_inches='tight', pad_inches=0.05, facecolor=C_NAVY_BG)
    plt.close(fig)
    print("Graphic 3 saved")

# ==========================================
# GRAPHIC 4: SLIDE 4 WORKFLOW & REST API
# ==========================================
def generate_graphic_4():
    fig, ax = setup_canvas(10, 5.5, dpi=140)
    
    add_card(ax, 2, 2, 96, 96, bg='#0D192E', border=C_CYAN, lw=1.8, radius=3)
    
    # Left: 10-Step Sequential Lifecycle (width 54)
    add_card(ax, 4, 5, 52, 90, bg=C_CARD_BG, border=C_CARD_BORDER, lw=1.4, radius=2.5)
    ax.text(30, 91, "10-STEP APPLICATION WORKFLOW", color=C_CYAN, fontsize=10, fontweight='bold', ha='center')
    
    wf_steps = [
        ("Step 1", "User opens the web application in browser", C_CYAN),
        ("Step 2", "User selects listing type: 'Lost' or 'Found'", C_CYAN_LIGHT),
        ("Step 3", "User enters item details & optional photo", C_WHITE),
        ("Step 4", "Frontend submits multipart/form-data payload", C_GREEN),
        ("Step 5", "Multer validates MIME type & 5 MB size limit", C_GOLD),
        ("Step 6", "Node.js saves image file into uploads/ directory", C_CORAL),
        ("Step 7", "Mongoose stores item document in MongoDB", C_CYAN),
        ("Step 8", "Frontend fetches active listings via REST API", C_CYAN_LIGHT),
        ("Step 9", "Users search & filter listings in real-time", C_WHITE),
        ("Step 10", "Item marked claimed/returned & moved to archive", C_GREEN)
    ]
    
    for i, (st, desc, col) in enumerate(wf_steps):
        sy = 82 - (i * 8.1)
        add_card(ax, 6, sy, 48, 6.8, bg='#132743', border='#1E3E66', lw=1, radius=1.2)
        # Step badge
        add_card(ax, 7.5, sy+1, 10, 4.8, bg='#1F3A60', border=col, lw=1, radius=1)
        ax.text(12.5, sy+3.4, st, color=col, fontsize=6.8, fontweight='bold', ha='center', va='center')
        ax.text(19.5, sy+3.4, desc, color=C_WHITE, fontsize=6.5, va='center')
        
    # Right: API Request-Response Cycle (width 38)
    add_card(ax, 58, 5, 38, 90, bg=C_CARD_BG, border=C_CARD_BORDER, lw=1.4, radius=2.5)
    ax.text(77, 91, "API REQUEST-RESPONSE CYCLE", color=C_CYAN, fontsize=10, fontweight='bold', ha='center')
    
    cycle_nodes = [
        ("CLIENT REQUEST", "GET /api/items?q=...&category=...\nPOST /api/items (multipart)\nPATCH /api/items/:id/claim", C_CYAN, 75),
        ("EXPRESS ROUTER", "MIME Validation · Regex Sanitizer\nError Handling Middleware", C_CYAN_LIGHT, 54),
        ("MONGOOSE & DB", "Item.find(filter) · Item.create()\nItem.findById() & save()", C_GOLD, 33),
        ("CLIENT RESPONSE", "HTTP 200 OK / 201 Created (JSON)\nHTTP 400 Bad Request / 404 Not Found", C_GREEN, 12)
    ]
    
    for title, desc, col, y in cycle_nodes:
        add_card(ax, 60.5, y, 33, 16, bg='#142847', border=col, lw=1.4, radius=2)
        ax.text(77, y+12.5, title, color=col, fontsize=7.5, fontweight='bold', ha='center')
        ax.text(77, y+6, desc, color=C_MUTED, fontsize=6.2, ha='center')
        if y > 20:
            ax.annotate("", xy=(77, y-4.5), xytext=(77, y),
                        arrowprops=dict(arrowstyle="->", color=C_WHITE, lw=1.4))
            
    fig.savefig('assets/slide4_api_workflow.png', bbox_inches='tight', pad_inches=0.05, facecolor=C_NAVY_BG)
    plt.close(fig)
    print("Graphic 4 saved")

# ==========================================
# GRAPHIC 5: SLIDE 5 DATABASE & TESTING
# ==========================================
def generate_graphic_5():
    fig, ax = setup_canvas(10, 5.5, dpi=140)
    
    add_card(ax, 2, 2, 96, 96, bg='#0D192E', border=C_CYAN, lw=1.8, radius=3)
    
    # Left: Database Schema Entity (width 45)
    add_card(ax, 4, 5, 44, 90, bg=C_CARD_BG, border=C_CARD_BORDER, lw=1.4, radius=2.5)
    ax.text(26, 91, "DATABASE SCHEMA: campus_lost_found", color=C_CYAN, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(26, 87.5, "Collection: items (Mongoose ODM Model)", color=C_SLATE, fontsize=7, ha='center')
    
    schema_fields = [
        ("_id", "ObjectId", "Primary key (auto-generated)"),
        ("title", "String", "Required, trimmed (Item name)"),
        ("description", "String", "Required, trimmed (Details)"),
        ("category", "String", "Required (Category enum)"),
        ("location", "String", "Required, trimmed (Campus zone)"),
        ("type", "String", "Required ('Lost' or 'Found')"),
        ("contact", "String", "Optional (Phone or email)"),
        ("photoUrl", "String", "Optional (/uploads/uuid.ext)"),
        ("archived", "Boolean", "Default: false (Active flag)"),
        ("createdAt", "Date", "Default: Date.now"),
        ("claimedAt", "Date", "Default: null (Timestamp)")
    ]
    
    for i, (f_name, f_type, f_desc) in enumerate(schema_fields):
        fy = 80 - (i * 7)
        add_card(ax, 6, fy, 40, 5.8, bg='#132743', border='#1E3E66', lw=0.8, radius=1)
        ax.text(7.5, fy+2.9, f_name, color=C_CYAN_LIGHT, fontsize=7, fontweight='bold', va='center')
        ax.text(20, fy+2.9, f_type, color=C_GOLD, fontsize=6.5, va='center')
        ax.text(28, fy+2.9, f_desc, color=C_MUTED, fontsize=5.8, va='center')
        
    # Right: Testing Scenarios Matrix (width 47)
    add_card(ax, 50, 5, 48, 90, bg=C_CARD_BG, border=C_CARD_BORDER, lw=1.4, radius=2.5)
    ax.text(74, 91, "VERIFICATION & TESTING CHECKLIST", color=C_CYAN, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(74, 87.5, "10 Comprehensive Test Cases Verified", color=C_GREEN, fontsize=7, fontweight='bold', ha='center')
    
    tests = [
        ("TC-01", "Create Lost listing without photo", "PASSED"),
        ("TC-02", "Create Found listing with image upload", "PASSED"),
        ("TC-03", "Upload image (JPG/PNG/WEBP/GIF)", "PASSED"),
        ("TC-04", "Enforce 5 MB maximum file upload limit", "PASSED"),
        ("TC-05", "Keyword search query (regex-safe)", "PASSED"),
        ("TC-06", "Filter items by category dropdown", "PASSED"),
        ("TC-07", "Filter items by campus location string", "PASSED"),
        ("TC-08", "Retrieve active items noticeboard", "PASSED"),
        ("TC-09", "Retrieve archived items board", "PASSED"),
        ("TC-10", "Claim/return item & move to archive", "PASSED")
    ]
    
    for i, (t_id, t_desc, t_stat) in enumerate(tests):
        ty = 80 - (i * 7.7)
        add_card(ax, 52, ty, 44, 6.4, bg='#142744', border=C_CARD_BORDER, lw=0.8, radius=1)
        ax.text(54, ty+3.2, t_id, color=C_CYAN, fontsize=6.8, fontweight='bold', va='center')
        ax.text(62, ty+3.2, t_desc, color=C_WHITE, fontsize=6.5, va='center')
        add_card(ax, 86, ty+1.2, 9, 4, bg='#064E3B', border=C_GREEN, lw=1, radius=0.8)
        ax.text(90.5, ty+3.2, t_stat, color=C_WHITE, fontsize=6, fontweight='bold', ha='center', va='center')
        
    fig.savefig('assets/slide5_database_testing.png', bbox_inches='tight', pad_inches=0.05, facecolor=C_NAVY_BG)
    plt.close(fig)
    print("Graphic 5 saved")

# ==========================================
# GRAPHIC 6: SLIDE 6 CAMPUS & ROADMAP
# ==========================================
def generate_graphic_6():
    fig, ax = setup_canvas(10, 5.5, dpi=140)
    
    add_card(ax, 2, 2, 96, 96, bg='#0D192E', border=C_CYAN, lw=1.8, radius=3)
    
    # Left: Roadmap of 10 Enhancements (width 54)
    add_card(ax, 4, 5, 52, 90, bg=C_CARD_BG, border=C_CARD_BORDER, lw=1.4, radius=2.5)
    ax.text(30, 91, "STRATEGIC FUTURE ROADMAP (10 PHASES)", color=C_CYAN, fontsize=9.5, fontweight='bold', ha='center')
    
    phases = [
        ("PHASE 1: AUTHENTICATION & ACCESS CONTROL", [
            "1. Student login and authentication (Campus SSO / LDAP)",
            "2. Role-based access control (Student, Staff, Admin)",
            "3. Admin moderation dashboard with item flags"
        ], C_CYAN),
        ("PHASE 2: NOTIFICATIONS & AI INTELLIGENCE", [
            "4. Automated email and SMS match notifications",
            "5. Secure in-app private contact communication",
            "6. AI-based computer vision image matching"
        ], C_CYAN_LIGHT),
        ("PHASE 3: ENTERPRISE SECURITY & PLATFORM SCALE", [
            "7. Cross-platform mobile app (React Native / Flutter)",
            "8. Enterprise rate limiting, CORS & CSRF defense",
            "9. Automated cloud database backups & recovery",
            "10. Image re-encoding, EXIF stripping & malware scanning"
        ], C_GOLD)
    ]
    
    curr_y = 85
    for p_title, p_items, p_col in phases:
        h = 6 + len(p_items) * 4.5
        curr_y -= (h + 2)
        add_card(ax, 6, curr_y, 48, h, bg='#132743', border=p_col, lw=1.2, radius=1.5)
        ax.text(8, curr_y + h - 3, p_title, color=p_col, fontsize=7, fontweight='bold')
        for idx, item in enumerate(p_items):
            ax.text(9, curr_y + h - 7.5 - (idx * 4.4), item, color=C_WHITE, fontsize=6.2)
            
    # Right: Thank You & Q&A Closer Banner (width 38)
    add_card(ax, 58, 5, 38, 90, bg=C_CARD_BG, border=C_CARD_BORDER, lw=1.4, radius=2.5)
    
    # Visual Campus Icon Badge
    add_card(ax, 61, 62, 32, 28, bg='#142744', border=C_CYAN, lw=1.6, radius=2)
    # Draw building icon with patches
    building_base = patches.Rectangle((70, 75), 14, 11, facecolor='#1E3D6B', edgecolor=C_CYAN_LIGHT, lw=1.2)
    ax.add_patch(building_base)
    roof_poly = patches.Polygon([[68, 86], [77, 91], [86, 86]], facecolor=C_CYAN, edgecolor=C_WHITE, lw=1)
    ax.add_patch(roof_poly)
    for px in [73, 77, 81]:
        ax.plot([px, px], [75, 84], color=C_WHITE, linewidth=1.2)
    ax.text(77, 68, "CAMPUS MANAGEMENT\nINFORMATION SYSTEM", color=C_CYAN_LIGHT,
            fontsize=8, fontweight='bold', ha='center', va='center')
    
    # Thank You Box
    add_card(ax, 61, 24, 32, 34, bg='#0A192F', border=C_CYAN, lw=2, radius=2)
    ax.text(77, 47, "THANK YOU!", color=C_WHITE, fontsize=18, fontweight='bold', ha='center', va='center')
    ax.text(77, 37, "Questions & Answers", color=C_CYAN, fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(77, 29, "Open for Faculty & Evaluator Feedback", color=C_MUTED, fontsize=7, ha='center', va='center')
    
    # Academic footer badge
    add_card(ax, 61, 8, 32, 12, bg='#172A45', border=C_CARD_BORDER, lw=1, radius=1.5)
    ax.text(77, 16.5, "MCA / Computer Science", color=C_CYAN_LIGHT, fontsize=7.5, fontweight='bold', ha='center')
    ax.text(77, 11.5, "Academic Project Viva Voce", color=C_MUTED, fontsize=6.8, ha='center')
    
    fig.savefig('assets/slide6_roadmap.png', bbox_inches='tight', pad_inches=0.05, facecolor=C_NAVY_BG)
    plt.close(fig)
    print("Graphic 6 saved")

if __name__ == '__main__':
    generate_graphic_1()
    generate_graphic_2()
    generate_graphic_3()
    generate_graphic_4()
    generate_graphic_5()
    generate_graphic_6()
    print("All 6 high-res graphics generated successfully!")
