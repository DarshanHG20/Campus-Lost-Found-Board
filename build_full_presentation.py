import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Professional Academic Color Palette
C_NAVY_BG = RGBColor(10, 25, 47)        # #0A192F Deep Midnight Navy
C_CARD_BG = RGBColor(17, 34, 64)        # #112240 Container Navy
C_CARD_BORDER = RGBColor(30, 58, 102)   # #1E3A66 Border
C_CARD_INNER = RGBColor(23, 42, 77)     # #172A4D Inner Box
C_DARK_INNER = RGBColor(13, 27, 49)     # #0D1B31 Darker Box
C_CYAN = RGBColor(0, 229, 255)          # #00E5FF Vibrant Cyan
C_CYAN_LIGHT = RGBColor(100, 255, 218)  # #64FFDA Soft Aqua
C_GREEN = RGBColor(16, 185, 129)        # #10B981 Emerald / Found
C_CORAL = RGBColor(255, 107, 107)       # #FF6B6B Coral / Lost
C_GOLD = RGBColor(245, 158, 11)         # #F59E0B Gold
C_WHITE = RGBColor(255, 255, 255)       # Pure White
C_MUTED = RGBColor(203, 213, 225)       # #CBD5E1 Ice Blue / Slate
C_SLATE = RGBColor(148, 163, 184)       # #94A3B8 Dim Slate

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

def add_para(tf, text, font_size=8, bold=False, color=C_WHITE, font_name=FONT_BODY, space_after=2, align=PP_ALIGN.LEFT):
    if len(tf.paragraphs) == 1 and tf.paragraphs[0].text == "":
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return p, run

def add_bullet_item(tf, prefix, text, font_size=8, prefix_color=C_WHITE, text_color=C_MUTED, space_after=2):
    p = tf.add_paragraph()
    p.space_after = Pt(space_after)
    r1 = p.add_run()
    r1.text = prefix + " "
    r1.font.name = FONT_HEADING
    r1.font.size = Pt(font_size)
    r1.font.bold = True
    r1.font.color.rgb = prefix_color
    
    r2 = p.add_run()
    r2.text = text
    r2.font.name = FONT_BODY
    r2.font.size = Pt(font_size)
    r2.font.bold = False
    r2.font.color.rgb = text_color
    return p

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    def set_background(slide):
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_NAVY_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, eyebrow, title, subtitle, slide_num):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(9.8), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        add_para(tf, eyebrow.upper(), font_size=8.5, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=2)
        add_para(tf, title, font_size=22, bold=True, color=C_WHITE, font_name=FONT_HEADING, space_after=2)
        add_para(tf, subtitle, font_size=10, bold=False, color=C_MUTED, font_name=FONT_BODY, space_after=0)
        
        # Badge Top-Right
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.6), Inches(0.4), Inches(2.133), Inches(0.9)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_CARD_BG
        badge.line.color.rgb = C_CYAN
        badge.line.width = Pt(1.2)
        
        btf = badge.text_frame
        btf.word_wrap = True
        btf.vertical_anchor = MSO_ANCHOR.MIDDLE
        btf.margin_left = btf.margin_right = Inches(0.1)
        
        add_para(btf, f"SLIDE {slide_num} / 06", font_size=11, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=1, align=PP_ALIGN.CENTER)
        add_para(btf, "MCA Academic Project Viva", font_size=8, bold=False, color=C_SLATE, font_name=FONT_BODY, space_after=0, align=PP_ALIGN.CENTER)

    def add_footer(slide, current_num):
        rule = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(7.05), Inches(12.133), Inches(0.015)
        )
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_CARD_BORDER
        rule.line.fill.background()
        
        ftb = slide.shapes.add_textbox(Inches(0.6), Inches(7.08), Inches(8.0), Inches(0.35))
        ftf = ftb.text_frame
        ftf.word_wrap = True
        ftf.margin_left = ftf.margin_right = ftf.margin_top = ftf.margin_bottom = 0
        add_para(ftf, "Campus Lost & Found Board  |  Full-Stack Node.js, Express & MongoDB Web Application",
                 font_size=8.5, color=C_SLATE, font_name=FONT_BODY)
        
        rtb = slide.shapes.add_textbox(Inches(9.0), Inches(7.08), Inches(3.733), Inches(0.35))
        rtf = rtb.text_frame
        rtf.margin_left = rtf.margin_right = rtf.margin_top = rtf.margin_bottom = 0
        add_para(rtf, f"Slide {current_num} of 6  •  Computer Science Postgraduate",
                 font_size=8.5, color=C_CYAN, font_name=FONT_BODY, align=PP_ALIGN.RIGHT)

    def add_card(slide, left, top, width, height, bg_col=C_CARD_BG, border_col=C_CARD_BORDER, border_width=1):
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        card.line.color.rgb = border_col
        card.line.width = Pt(border_width)
        return card

    # =========================================================================
    # SLIDE 1: PROJECT INTRODUCTION
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_background(s1)
    add_header(s1, "Academic Project Presentation • MCA / Computer Science",
               "CAMPUS LOST & FOUND BOARD",
               "A Responsive Web Noticeboard for Campus Community Item Reporting & Recovery", "01")
    add_footer(s1, "01")
    
    meta_items = [
        ("PROJECT NAME", "Campus Lost & Found Board", C_CYAN),
        ("PROJECT CATEGORY", "Web-Based Application", C_GREEN),
        ("PROJECT DOMAIN", "Campus Management & Information Sharing", C_GOLD)
    ]
    for i, (m_lbl, m_val, m_col) in enumerate(meta_items):
        mx = 0.6 + i * 4.1
        add_card(s1, mx, 1.6, 3.933, 0.62, bg_col=C_DARK_INNER, border_col=m_col, border_width=1.2)
        tb = s1.shapes.add_textbox(Inches(mx + 0.15), Inches(1.63), Inches(3.633), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        add_para(tf, m_lbl, font_size=7.5, bold=True, color=m_col, font_name=FONT_CODE, space_after=1)
        add_para(tf, m_val, font_size=9.5, bold=True, color=C_WHITE, font_name=FONT_HEADING, space_after=0)

    # Left Column: Problem, Solution & Objectives
    add_card(s1, 0.6, 2.35, 6.4, 4.55, bg_col=C_CARD_BG, border_col=C_CARD_BORDER)
    
    tb_prob = s1.shapes.add_textbox(Inches(0.8), Inches(2.45), Inches(6.0), Inches(1.05))
    tf_prob = tb_prob.text_frame
    tf_prob.word_wrap = True
    tf_prob.margin_left = tf_prob.margin_top = tf_prob.margin_right = tf_prob.margin_bottom = 0
    add_para(tf_prob, "PROBLEM STATEMENT", font_size=9.5, bold=True, color=C_CORAL, font_name=FONT_CODE, space_after=2)
    add_para(tf_prob, "Students frequently lose personal belongings such as ID cards, books, wallets, keys, water bottles, and electronic devices inside campus premises. Traditional reporting methods (physical noticeboards, word of mouth, informal chats) are fragmented, slow, and make it difficult to connect the person who lost an item with the finder.",
             font_size=8.5, bold=False, color=C_MUTED, font_name=FONT_BODY, space_after=0)

    tb_sol = s1.shapes.add_textbox(Inches(0.8), Inches(3.52), Inches(6.0), Inches(0.8))
    tf_sol = tb_sol.text_frame
    tf_sol.word_wrap = True
    tf_sol.margin_left = tf_sol.margin_top = tf_sol.margin_right = tf_sol.margin_bottom = 0
    add_para(tf_sol, "PROPOSED SOLUTION", font_size=9.5, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=2)
    add_para(tf_sol, "Develop a centralized, responsive web-based platform where campus members can report lost or found items, upload photographs, search active listings in real time, and mark items as claimed or returned.",
             font_size=8.5, bold=False, color=C_WHITE, font_name=FONT_BODY, space_after=0)

    tb_obj = s1.shapes.add_textbox(Inches(0.8), Inches(4.35), Inches(6.0), Inches(2.45))
    tf_obj = tb_obj.text_frame
    tf_obj.word_wrap = True
    tf_obj.margin_left = tf_obj.margin_top = tf_obj.margin_right = tf_obj.margin_bottom = 0
    add_para(tf_obj, "CORE PROJECT OBJECTIVES (6 PILLARS)", font_size=9.5, bold=True, color=C_GREEN, font_name=FONT_CODE, space_after=3)
    
    objectives = [
        ("1. Centralized Platform:", "Establish a single official noticeboard accessible to all departments."),
        ("2. Dual Reporting Flow:", "Streamline submission of both Lost items and Found items."),
        ("3. Photo Verification:", "Support JPG, PNG, WEBP, and GIF image uploads up to 5 MB."),
        ("4. Search & Filtering:", "Enable free-text queries, category filters, and campus location tags."),
        ("5. Lifecycle Archiving:", "Automatically segregate active listings from claimed/returned items."),
        ("6. Campus Connectivity:", "Enhance communication and trust among students, faculty, and staff.")
    ]
    for o_pre, o_desc in objectives:
        add_bullet_item(tf_obj, o_pre, o_desc, font_size=8.2, prefix_color=C_CYAN_LIGHT, text_color=C_MUTED, space_after=1.5)

    add_card(s1, 7.15, 2.35, 5.58, 4.55, bg_col=C_CARD_BG, border_col=C_CYAN, border_width=1.5)
    s1.shapes.add_picture('assets/slide1_hero.png', Inches(7.28), Inches(2.48), Inches(5.32), Inches(3.45))
    
    add_card(s1, 7.28, 6.02, 5.32, 0.76, bg_col=C_DARK_INNER, border_col=C_CARD_BORDER)
    tb_cap = s1.shapes.add_textbox(Inches(7.4), Inches(6.05), Inches(5.08), Inches(0.7))
    tf_cap = tb_cap.text_frame
    tf_cap.word_wrap = True
    tf_cap.margin_left = tf_cap.margin_top = tf_cap.margin_right = tf_cap.margin_bottom = 0
    add_para(tf_cap, "ACADEMIC SCOPE & AUDIENCE", font_size=8, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=1)
    add_para(tf_cap, "Designed for MCA project evaluation, faculty evaluators, and real-world campus deployment.",
             font_size=8, color=C_WHITE, font_name=FONT_BODY, space_after=0)

    # =========================================================================
    # SLIDE 2: FEATURES AND USER INTERFACE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_background(s2)
    add_header(s2, "Functional Specifications & UI Architecture",
               "CORE FEATURES AND FUNCTIONALITIES",
               "Comprehensive End-to-End Capabilities from Reporting to Multi-Criteria Discovery and Archiving", "02")
    add_footer(s2, "02")

    feature_groups = [
        ("REPORTING & MULTIMEDIA CAPABILITIES", C_CYAN, [
            ("• 1. Lost Item Reporting:", "Submit title, description, category, campus location, and optional contact details."),
            ("• 2. Found Item Reporting:", "Report discovered items with specific pickup location to help rightful owners."),
            ("• 3. Image Upload System:", "Upload item photos in JPG, PNG, WEBP, or GIF formats (maximum file size: 5 MB).")
        ], 1.6, 1.65),
        ("SEARCH & MULTI-CRITERIA FILTERING", C_GREEN, [
            ("• 4. Search Functionality:", "Free-text regex-safe keyword query matching title, description, and location."),
            ("• 5. Category Filtering:", "Filter by 7 categories: Electronics, Accessories, Clothing, Books, Keys/Cards, Bags, Other."),
            ("• 6. Location Filtering:", "Target campus zones: Library, Classrooms, Cafeteria, Science Labs, Auditoriums.")
        ], 3.35, 1.65),
        ("LIFECYCLE MANAGEMENT & RESPONSIVENESS", C_GOLD, [
            ("• 7. Claim & Return Verification:", "One-click handover confirmation marking items as claimed/returned."),
            ("• 8. Archive Management:", "Claimed listings are moved to archived view, preserving board cleanliness."),
            ("• 9. Responsive Interface:", "Adaptive CSS grid/flexbox supporting desktop, tablet, and mobile screens.")
        ], 5.1, 1.8)
    ]

    for g_title, g_col, g_feats, g_top, g_h in feature_groups:
        add_card(s2, 0.6, g_top, 5.5, g_h, bg_col=C_CARD_BG, border_col=g_col, border_width=1.2)
        tb = s2.shapes.add_textbox(Inches(0.75), Inches(g_top + 0.08), Inches(5.2), Inches(g_h - 0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        add_para(tf, g_title, font_size=8.5, bold=True, color=g_col, font_name=FONT_CODE, space_after=2)
        for f_pre, f_desc in g_feats:
            add_bullet_item(tf, f_pre, f_desc, font_size=8, prefix_color=C_WHITE, text_color=C_MUTED, space_after=1.5)

    add_card(s2, 6.25, 1.6, 6.48, 5.3, bg_col=C_CARD_BG, border_col=C_CYAN, border_width=1.5)
    s2.shapes.add_picture('assets/slide2_ui_mockup.png', Inches(6.38), Inches(1.72), Inches(6.22), Inches(3.72))
    
    add_card(s2, 6.38, 5.54, 6.22, 1.24, bg_col=C_DARK_INNER, border_col=C_CARD_BORDER)
    tb_dist = s2.shapes.add_textbox(Inches(6.5), Inches(5.6), Inches(5.98), Inches(1.12))
    tf_dist = tb_dist.text_frame
    tf_dist.word_wrap = True
    tf_dist.margin_left = tf_dist.margin_top = tf_dist.margin_right = tf_dist.margin_bottom = 0
    add_para(tf_dist, "ACTIVE VS ARCHIVED LISTINGS ARCHITECTURE", font_size=8.5, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=2)
    add_bullet_item(tf_dist, "• Active Board:", "Displays open Lost and Found notices with prominent color badges, contact info, and active 'Mark as Claimed' buttons.",
                    font_size=8, prefix_color=C_GREEN, text_color=C_WHITE, space_after=1.5)
    add_bullet_item(tf_dist, "• Archived Board:", "Displays returned items with 'CLAIMED' stamp and resolution date, keeping the active board clutter-free.",
                    font_size=8, prefix_color=C_SLATE, text_color=C_MUTED, space_after=0)

    # =========================================================================
    # SLIDE 3: TECHNOLOGY STACK AND SYSTEM ARCHITECTURE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_background(s3)
    add_header(s3, "System Design, Engineering & Component Hierarchy",
               "TECHNOLOGY STACK AND ARCHITECTURE",
               "Multi-Tier Architecture Built with Node.js, Express.js, MongoDB, Mongoose, and Multer", "03")
    add_footer(s3, "03")

    tech_stacks = [
        ("FRONTEND PRESENTATION LAYER", C_CYAN, [
            ("• HTML5:", "Semantic document structure, form controls, and accessible tags."),
            ("• CSS3:", "Responsive grid and flexbox, custom variables, and modern aesthetics."),
            ("• JavaScript (ES6+):", "Client-side dynamic UI rendering, Fetch API calls, and instant filters.")
        ], 1.6, 1.25),
        ("BACKEND ENGINE & REST ROUTING", C_GREEN, [
            ("• Node.js 18+:", "Asynchronous, event-driven runtime handling concurrent campus traffic."),
            ("• Express.js:", "REST API routing, JSON body-parser, static uploads, and error handlers.")
        ], 2.95, 1.15),
        ("DATABASE & OBJECT MODELING", C_GOLD, [
            ("• MongoDB:", "High-performance NoSQL document database storing campus item records."),
            ("• Mongoose 9+:", "Schema modeling, strict data type casting, validation, and queries.")
        ], 4.2, 1.15),
        ("STORAGE & ENVIRONMENT MANAGEMENT", C_CORAL, [
            ("• Multer:", "Memory buffer streaming and fileFilter validating JPG/PNG/WEBP/GIF."),
            ("• Node.js fs module:", "Filesystem persistence saving image buffers into uploads/ directory."),
            ("• dotenv & npm:", "Secure environment variables (PORT, MONGO_URI) and dependencies.")
        ], 5.45, 1.45)
    ]

    for t_title, t_col, t_items, t_top, t_h in tech_stacks:
        add_card(s3, 0.6, t_top, 5.5, t_h, bg_col=C_CARD_BG, border_col=t_col, border_width=1.2)
        tb = s3.shapes.add_textbox(Inches(0.75), Inches(t_top + 0.08), Inches(5.2), Inches(t_h - 0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        add_para(tf, t_title, font_size=8.5, bold=True, color=t_col, font_name=FONT_CODE, space_after=2)
        for pre, desc in t_items:
            add_bullet_item(tf, pre, desc, font_size=8, prefix_color=C_WHITE, text_color=C_MUTED, space_after=1)

    add_card(s3, 6.25, 1.6, 6.48, 5.3, bg_col=C_CARD_BG, border_col=C_CYAN, border_width=1.5)
    s3.shapes.add_picture('assets/slide3_architecture.png', Inches(6.38), Inches(1.72), Inches(6.22), Inches(5.06))

    # =========================================================================
    # SLIDE 4: SYSTEM WORKFLOW AND REST API
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_background(s4)
    add_header(s4, "Data Lifecycle & RESTful Web Service Design",
               "APPLICATION WORKFLOW AND API DESIGN",
               "10-Step Operational Workflow and Complete REST API Specification with Query Filters", "04")
    add_footer(s4, "04")

    # Left Column: 10-Step Workflow
    add_card(s4, 0.6, 1.6, 5.5, 5.3, bg_col=C_CARD_BG, border_col=C_CARD_BORDER)
    tb_wf = s4.shapes.add_textbox(Inches(0.78), Inches(1.72), Inches(5.14), Inches(5.06))
    tf_wf = tb_wf.text_frame
    tf_wf.word_wrap = True
    tf_wf.margin_left = tf_wf.margin_top = tf_wf.margin_right = tf_wf.margin_bottom = 0
    add_para(tf_wf, "COMPLETE 10-STEP APPLICATION WORKFLOW", font_size=9.5, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=4)

    steps_text = [
        ("Step 1:", "User accesses the Campus Lost & Found Board web application."),
        ("Step 2:", "User selects reporting intention: 'Lost' or 'Found' item."),
        ("Step 3:", "User enters item details (Title, Description, Category, Location, Contact, Photo)."),
        ("Step 4:", "Frontend serializes form attributes into a multipart/form-data payload."),
        ("Step 5:", "Multer inspects file buffer, validates MIME type and 5 MB size limit."),
        ("Step 6:", "Node.js fs module persists binary file into uploads/ with crypto UUID."),
        ("Step 7:", "Mongoose schema stores item document into MongoDB campus_lost_found DB."),
        ("Step 8:", "Frontend fetches active listings via asynchronous REST API GET request."),
        ("Step 9:", "Students search listings by keyword, category, and location in real time."),
        ("Step 10:", "When returned, listing is marked claimed via PATCH API and archived.")
    ]
    for st_num, st_desc in steps_text:
        add_bullet_item(tf_wf, st_num, st_desc, font_size=8, prefix_color=C_CYAN_LIGHT, text_color=C_WHITE, space_after=2.2)

    # Right Column Top: REST API Table
    add_card(s4, 6.25, 1.6, 6.48, 2.3, bg_col=C_CARD_BG, border_col=C_CYAN, border_width=1.2)
    table_shape = s4.shapes.add_table(4, 4, Inches(6.38), Inches(1.72), Inches(6.22), Inches(2.05))
    table = table_shape.table
    table.columns[0].width = Inches(1.1)
    table.columns[1].width = Inches(1.85)
    table.columns[2].width = Inches(2.15)
    table.columns[3].width = Inches(1.12)
    
    api_headers = ["Method", "Endpoint", "Purpose", "Payload"]
    for c_idx, h_text in enumerate(api_headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(19, 42, 77)
        tf = cell.text_frame
        tf.word_wrap = True
        add_para(tf, h_text, font_size=8.5, bold=True, color=C_CYAN, font_name=FONT_CODE, align=PP_ALIGN.CENTER)
        
    api_rows = [
        ("GET", "/api/items", "Retrieve & search listings", "Query Params"),
        ("POST", "/api/items", "Create new lost/found item", "multipart/form"),
        ("PATCH", "/api/items/:id/claim", "Mark item claimed/archived", "URL Param")
    ]
    for r_idx, row in enumerate(api_rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_DARK_INNER if r_idx % 2 == 0 else C_CARD_BG
            tf = cell.text_frame
            tf.word_wrap = True
            col = C_GREEN if val == "GET" else (C_CORAL if val == "POST" else (C_GOLD if val == "PATCH" else C_WHITE))
            align = PP_ALIGN.CENTER if c_idx == 0 or c_idx == 3 else PP_ALIGN.LEFT
            add_para(tf, val, font_size=7.8, bold=(c_idx == 0), color=col, font_name=FONT_CODE if c_idx < 2 else FONT_BODY, align=align)

    # Right Column Middle: Query Parameters Card
    add_card(s4, 6.25, 4.0, 6.48, 1.45, bg_col=C_DARK_INNER, border_col=C_CARD_BORDER)
    tb_qp = s4.shapes.add_textbox(Inches(6.4), Inches(4.06), Inches(6.18), Inches(1.33))
    tf_qp = tb_qp.text_frame
    tf_qp.word_wrap = True
    tf_qp.margin_left = tf_qp.margin_top = tf_qp.margin_right = tf_qp.margin_bottom = 0
    add_para(tf_qp, "API QUERY PARAMETERS & MULTIPART SPECIFICATIONS", font_size=8.5, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=2)
    
    params_info = [
        ("• q:", "Free-text keyword regex search matching title, description, location, category."),
        ("• category:", "Filters listings by specific category (e.g. 'Electronics', 'Keys & Cards')."),
        ("• location:", "Filters by campus location (e.g. 'Library', 'Classroom 204')."),
        ("• status:", "Listing lifecycle state: 'active' (default) or 'archived' (claimed items).")
    ]
    for p_name, p_desc in params_info:
        add_bullet_item(tf_qp, p_name, p_desc, font_size=7.5, prefix_color=C_CYAN_LIGHT, text_color=C_MUTED, space_after=1)
        
    add_para(tf_qp, "NOTE: POST /api/items requires multipart/form-data with photo field name 'photo' (max 5 MB).",
             font_size=7.2, bold=True, color=C_GOLD, font_name=FONT_CODE, space_after=0)

    # Right Column Bottom: Request-Response Flow Diagram
    add_card(s4, 6.25, 5.55, 6.48, 1.35, bg_col=C_CARD_BG, border_col=C_CARD_BORDER)
    s4.shapes.add_picture('assets/slide4_api_workflow.png', Inches(6.35), Inches(5.6), Inches(6.28), Inches(1.25))

    # =========================================================================
    # SLIDE 5: DATABASE, SECURITY AND TESTING
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_background(s5)
    add_header(s5, "Data Modeling, Hardening & Quality Assurance",
               "DATABASE MANAGEMENT, SECURITY AND TESTING",
               "Mongoose Schema Architecture, Defense-in-Depth Measures, and 10 Verified Test Scenarios", "05")
    add_footer(s5, "05")

    # Column 1: Database Management (Width: 3.8 inches)
    add_card(s5, 0.6, 1.6, 3.8, 5.3, bg_col=C_CARD_BG, border_col=C_CYAN, border_width=1.2)
    tb_db = s5.shapes.add_textbox(Inches(0.75), Inches(1.72), Inches(3.5), Inches(5.06))
    tf_db = tb_db.text_frame
    tf_db.word_wrap = True
    tf_db.margin_left = tf_db.margin_top = tf_db.margin_right = tf_db.margin_bottom = 0
    add_para(tf_db, "DATABASE ARCHITECTURE", font_size=9.5, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=2)
    add_para(tf_db, "Database: campus_lost_found\nCollection: items (Mongoose ODM)", font_size=8, bold=True, color=C_CYAN_LIGHT, font_name=FONT_CODE, space_after=4)

    fields = [
        ("• title (String):", "Required, trimmed (Item title)"),
        ("• description (String):", "Required, trimmed (Details)"),
        ("• category (String):", "Required (Category enum)"),
        ("• location (String):", "Required, trimmed (Campus zone)"),
        ("• type (String):", "Required (Enum: 'Lost' | 'Found')"),
        ("• contact (String):", "Optional (Phone or email)"),
        ("• photoUrl (String):", "Default: null (Relative URL)"),
        ("• archived (Boolean):", "Default: false (Active flag)"),
        ("• createdAt (Date):", "Default: Date.now (Timestamp)"),
        ("• claimedAt (Date):", "Default: null (Claim timestamp)")
    ]
    for fn, fd in fields:
        add_bullet_item(tf_db, fn, fd, font_size=7.5, prefix_color=C_WHITE, text_color=C_MUTED, space_after=1.5)
        
    add_para(tf_db, "Database Operations:", font_size=8, bold=True, color=C_CYAN_LIGHT, font_name=FONT_HEADING, space_after=1)
    add_para(tf_db, "MongoDB stores flexible BSON documents. Mongoose enforces strict validation, type casting, schema indexes, and virtual id mapping.",
             font_size=7.5, bold=False, color=C_WHITE, font_name=FONT_BODY, space_after=0)

    # Column 2: Security & Validation (Width: 3.8 inches)
    add_card(s5, 4.6, 1.6, 3.8, 5.3, bg_col=C_CARD_BG, border_col=C_GREEN, border_width=1.2)
    tb_sec = s5.shapes.add_textbox(Inches(4.75), Inches(1.72), Inches(3.5), Inches(5.06))
    tf_sec = tb_sec.text_frame
    tf_sec.word_wrap = True
    tf_sec.margin_left = tf_sec.margin_top = tf_sec.margin_right = tf_sec.margin_bottom = 0
    add_para(tf_sec, "SECURITY & VALIDATION", font_size=9.5, bold=True, color=C_GREEN, font_name=FONT_CODE, space_after=2)
    add_para(tf_sec, "IMPLEMENTED DEMO SAFEGUARDS:", font_size=8, bold=True, color=C_WHITE, font_name=FONT_CODE, space_after=3)

    sec_rules = [
        ("✓ 1. MIME Validation:", "Only JPG, PNG, WEBP, GIF accepted."),
        ("✓ 2. File Size Limit:", "Strict 5 MB limit via Multer limits."),
        ("✓ 3. XSS Sanitization:", "escapeHtml() sanitizes all output."),
        ("✓ 4. Input Trimming:", "Trims title, description, category, loc."),
        ("✓ 5. Regex Escaping:", "escapeRegex() blocks query crashes."),
        ("✓ 6. Privacy Protection:", "Voluntary contact details; safe handover.")
    ]
    for sn, sd in sec_rules:
        add_bullet_item(tf_sec, sn, sd, font_size=7.8, prefix_color=C_GREEN, text_color=C_MUTED, space_after=1.5)

    add_para(tf_sec, "DISTINCTION: PRODUCTION ROADMAP", font_size=8.5, bold=True, color=C_GOLD, font_name=FONT_CODE, space_after=2)
    prod_points = [
        ("• Student Auth:", "Institutional SSO / LDAP campus credentials."),
        ("• Role Control:", "Role-based authorization & staff moderation."),
        ("• Rate Limiting:", "Express rate-limiter prevents DoS abuse."),
        ("• CSRF Tokens:", "Token verification on state mutations."),
        ("• File Scanning:", "Image re-encoding & automated antivirus scans.")
    ]
    for pp_pre, pp_desc in prod_points:
        add_bullet_item(tf_sec, pp_pre, pp_desc, font_size=7.5, prefix_color=C_GOLD, text_color=C_WHITE, space_after=1.2)

    # Column 3: Testing Scenarios & Verification Matrix (Width: 4.133 inches)
    add_card(s5, 8.6, 1.6, 4.133, 5.3, bg_col=C_CARD_BG, border_col=C_CYAN, border_width=1.2)
    tb_tst = s5.shapes.add_textbox(Inches(8.75), Inches(1.72), Inches(3.833), Inches(5.06))
    tf_tst = tb_tst.text_frame
    tf_tst.word_wrap = True
    tf_tst.margin_left = tf_tst.margin_top = tf_tst.margin_right = tf_tst.margin_bottom = 0
    add_para(tf_tst, "TESTING & VERIFICATION MATRIX", font_size=9.5, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=2)
    add_para(tf_tst, "10 ACADEMIC TEST CASES (ALL VERIFIED):", font_size=8, bold=True, color=C_WHITE, font_name=FONT_CODE, space_after=3)

    test_cases = [
        ("[PASS] TC-01:", "Create a Lost listing (Verified 201 Created)"),
        ("[PASS] TC-02:", "Create a Found listing (Verified 201 Created)"),
        ("[PASS] TC-03:", "Upload image (JPG/PNG) (Stored in uploads/)"),
        ("[PASS] TC-04:", "Search using free-text keyword (Regex safe)"),
        ("[PASS] TC-05:", "Filter listings by category (Exact category match)"),
        ("[PASS] TC-06:", "Filter listings by location (Case-insensitive)"),
        ("[PASS] TC-07:", "Retrieve active items board (archived: false)"),
        ("[PASS] TC-08:", "Retrieve archived items board (archived: true)"),
        ("[PASS] TC-09:", "Claim/return item (PATCH) (archived set to true)"),
        ("[PASS] TC-10:", "Reject invalid format / >5MB (HTTP 400 Rejected)")
    ]
    for tc_pre, tc_desc in test_cases:
        add_bullet_item(tf_tst, tc_pre, tc_desc, font_size=7.5, prefix_color=C_GREEN, text_color=C_MUTED, space_after=1.5)
        
    # Testing Badge Card
    add_card(s5, 8.75, 5.3, 3.833, 1.45, bg_col=C_DARK_INNER, border_col=C_GREEN, border_width=1)
    tb_tstat = s5.shapes.add_textbox(Inches(8.85), Inches(5.38), Inches(3.633), Inches(1.3))
    tf_tstat = tb_tstat.text_frame
    tf_tstat.word_wrap = True
    tf_tstat.margin_left = tf_tstat.margin_top = tf_tstat.margin_right = tf_tstat.margin_bottom = 0
    add_para(tf_tstat, "ACADEMIC QA VERIFICATION STATUS", font_size=8, bold=True, color=C_GREEN, font_name=FONT_CODE, space_after=2)
    add_para(tf_tstat, "• Automated E2E verification test suite executed successfully.\n• Zero regression on regex injections, oversized uploads, and invalid ObjectIds.\n• Database atomicity and file system sync confirmed.",
             font_size=7.3, color=C_WHITE, font_name=FONT_BODY, space_after=0)

    # =========================================================================
    # SLIDE 6: RESULTS, FUTURE ENHANCEMENTS AND CONCLUSION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_background(s6)
    add_header(s6, "Academic Evaluation, Roadmap & Concluding Summary",
               "PROJECT OUTCOME AND FUTURE SCOPE",
               "Expected Deliverables, Strategic 10-Point Enhancement Roadmap, and Concluding Remarks", "06")
    add_footer(s6, "06")

    # Column 1: Expected Outcomes (Width: 3.7 inches)
    add_card(s6, 0.6, 1.6, 3.7, 5.3, bg_col=C_CARD_BG, border_col=C_CYAN, border_width=1.2)
    tb_res = s6.shapes.add_textbox(Inches(0.75), Inches(1.72), Inches(3.4), Inches(5.06))
    tf_res = tb_res.text_frame
    tf_res.word_wrap = True
    tf_res.margin_left = tf_res.margin_top = tf_res.margin_right = tf_res.margin_bottom = 0
    add_para(tf_res, "EXPECTED PROJECT OUTCOMES", font_size=9.5, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=4)

    outcomes = [
        ("• Centralized Campus Hub:", "Eliminates scattered physical notices and unofficial social media posts with one official board."),
        ("• Faster Identification:", "Photographic evidence and detailed physical descriptions enable rapid identification of lost property."),
        ("• Frictionless Reporting:", "Straightforward submission form allows any student or staff member to post notices in under 2 minutes."),
        ("• Precision Search & Filter:", "Real-time search across categories and campus locations quickly narrows down relevant items."),
        ("• Organized Item Archiving:", "Claimed listings are cleanly segregated from active listings, keeping the active board relevant."),
        ("• Campus Communication:", "Fosters a supportive community culture of honesty, responsibility, and mutual assistance.")
    ]
    for o_pre, o_desc in outcomes:
        add_bullet_item(tf_res, o_pre, o_desc, font_size=8, prefix_color=C_WHITE, text_color=C_MUTED, space_after=2.5)

    # Column 2: 10 Future Enhancements (Width: 4.1 inches)
    add_card(s6, 4.5, 1.6, 4.1, 5.3, bg_col=C_CARD_BG, border_col=C_GOLD, border_width=1.2)
    tb_fut = s6.shapes.add_textbox(Inches(4.65), Inches(1.72), Inches(3.8), Inches(5.06))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True
    tf_fut.margin_left = tf_fut.margin_top = tf_fut.margin_right = tf_fut.margin_bottom = 0
    add_para(tf_fut, "FUTURE ENHANCEMENTS (10 MILESTONES)", font_size=9.5, bold=True, color=C_GOLD, font_name=FONT_CODE, space_after=4)

    enhancements = [
        ("1. Student Authentication:", "Institutional SSO / LDAP campus logins."),
        ("2. Role-Based Access:", "Student, Faculty, and Campus Security admin roles."),
        ("3. Moderation Dashboard:", "Admin item verification and content flagging."),
        ("4. Automated Notifications:", "Email and SMS alerts on potential keyword matches."),
        ("5. Private Communication:", "In-app safe messaging without exposing phone numbers."),
        ("6. AI Image Matching:", "Computer vision visual similarity search for items."),
        ("7. Mobile App Integration:", "Native iOS and Android apps using React Native / Flutter."),
        ("8. Advanced Security:", "Express rate-limiting and CSRF protection for scale."),
        ("9. Database Resilience:", "Automated cloud backups (AWS S3) and disaster recovery."),
        ("10. Image Sanitization:", "Automated re-encoding, EXIF stripping, and malware scan.")
    ]
    for enh_pre, enh_desc in enhancements:
        add_bullet_item(tf_fut, enh_pre, enh_desc, font_size=7.8, prefix_color=C_GOLD, text_color=C_WHITE, space_after=1.8)

    # Column 3: Conclusion & Closing Viva Card (Width: 3.933 inches)
    add_card(s6, 8.8, 1.6, 3.933, 2.5, bg_col=C_DARK_INNER, border_col=C_CYAN, border_width=1.4)
    tb_concl = s6.shapes.add_textbox(Inches(8.95), Inches(1.72), Inches(3.633), Inches(2.25))
    tf_concl = tb_concl.text_frame
    tf_concl.word_wrap = True
    tf_concl.margin_left = tf_concl.margin_top = tf_concl.margin_right = tf_concl.margin_bottom = 0
    add_para(tf_concl, "PROJECT CONCLUSION", font_size=9.5, bold=True, color=C_CYAN, font_name=FONT_CODE, space_after=3)
    add_para(tf_concl, "Campus Lost & Found Board provides a centralized, user-friendly digital solution for managing lost and found items within educational institutions.\n\nIt simplifies reporting, searching, identifying, and returning lost belongings through a responsive web application powered by Node.js, Express.js, and MongoDB.",
             font_size=8.2, bold=False, color=C_WHITE, font_name=FONT_BODY, space_after=0)

    # Closing Viva Card: Thank You & Q&A
    add_card(s6, 8.8, 4.25, 3.933, 2.65, bg_col=C_CARD_BG, border_col=C_CYAN_LIGHT, border_width=1.8)
    tb_thanks = s6.shapes.add_textbox(Inches(8.95), Inches(4.4), Inches(3.633), Inches(2.35))
    tf_thanks = tb_thanks.text_frame
    tf_thanks.word_wrap = True
    tf_thanks.margin_left = tf_thanks.margin_top = tf_thanks.margin_right = tf_thanks.margin_bottom = 0
    
    add_para(tf_thanks, "THANK YOU!", font_size=24, bold=True, color=C_CYAN, font_name=FONT_HEADING, space_after=2, align=PP_ALIGN.CENTER)
    add_para(tf_thanks, "Questions & Answers", font_size=13, bold=True, color=C_WHITE, font_name=FONT_HEADING, space_after=4, align=PP_ALIGN.CENTER)
    add_para(tf_thanks, "Open for Project Evaluation & Feedback\nMCA / Computer Science Academic Viva",
             font_size=8.5, bold=False, color=C_MUTED, font_name=FONT_BODY, space_after=0, align=PP_ALIGN.CENTER)

    # Save PPTX
    out_path = "Campus_Lost_Found_Board_Presentation.pptx"
    prs.save(out_path)
    print(f"Presentation saved successfully as: {out_path}")
    return out_path

if __name__ == '__main__':
    create_presentation()
