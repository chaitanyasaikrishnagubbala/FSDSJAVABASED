r"""
Script to populate the exact template from:
C:\Users\chait\Downloads\Updated Standard_Template_PO_PSO_SDG_Alignment.doc
with complete, verified RentRide Project Alignment data.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
import os

TEMPLATE_DOCX = os.path.join(os.getcwd(), "extracted_template.docx")
OUTPUT_DOCX = os.path.join(os.getcwd(), "project-documentation", "Completed_RentRide_PO_PSO_SDG_Alignment.docx")

def format_cell(cell, text, bold_prefix=None, font_size=9.5, font_name="Calibri"):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.bold = True
        r_b.font.name = font_name
        r_b.font.size = Pt(font_size)
        r_b.font.color.rgb = RGBColor(15, 23, 42)
    r_t = p.add_run(text)
    r_t.font.name = font_name
    r_t.font.size = Pt(font_size)
    r_t.font.color.rgb = RGBColor(30, 41, 59)

def populate_alignment_document():
    doc = docx.Document(TEMPLATE_DOCX)

    # 1. Populate Table 1: Student and Subject Details
    t1 = doc.tables[0]
    details = [
        ("Student Name", "GUBBALA CHAITANYA SAI KRISHNA"),
        ("Roll Number", "24761A0517"),
        ("Year / Semester / Section", "IV Year / I Semester / B.Tech CSE"),
        ("Department / Programme", "Department of Computer Science and Engineering / B.Tech"),
        ("Subject Name and Code", "Full Stack Web Development & Project Work (CS701)"),
        ("Faculty Name", "Faculty In-Charge / Project Guide (Department of CSE)"),
        ("Project Title / Assignment / Case Study", "Vehicle Rental System (RentRide) — Full-Stack Web Application"),
        ("Technology / Tools Used", "Java 21 LTS, Java EE Servlets, JSP, JDBC, MySQL 8.0, Apache Tomcat 9.0, jBCrypt 0.4, Vanilla CSS3, Selenium WebDriver 4.x")
    ]
    for row_idx, (label, val) in enumerate(details):
        t1.rows[row_idx].cells[1].text = val
        p = t1.rows[row_idx].cells[1].paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = (row_idx in [0, 1, 6]) # Bold for Name, Roll No, Project Title

    # 2. Populate Section 2: Project / Subject Activity Summary Paragraphs
    summary_replacements = {
        "Minimum 3 to 5 lines required": [
            # P9: Problem statement
            ("Traditional vehicle rental operations suffer from manual record-keeping inaccuracies, lack of real-time inventory visibility, double-booking collisions, and opaque pricing structures. Offline rental processes create customer friction, manual billing discrepancies, and insecure credential storage. The RentRide Vehicle Rental System addresses these challenges by delivering an automated, web-based digital ecosystem providing transparent self-service vehicle discovery, concurrency-protected reservations, automated price estimation, and centralized fleet governance."),
            # P13: Brief description of solution
            ("RentRide is an enterprise-grade full-stack web application engineered on a classic Three-Tier Architectural model (JSP presentation, Java EE Servlet controllers, and MySQL 8.0 persistence via JDBC). Key features include: real vehicle photography cards with transparent daily rates; dynamic client-side rental price computation; atomic reservation booking with automatic date overlap rejection via pessimistic row locking; a mock development payment sandbox (Card, UPI, Netbanking); customer reservation dashboards with self-service cancellation; and an executive administration console with gross revenue KPI analytics and fleet governance controls."),
            # P17: Expected or observed outcomes
            ("The application was deployed on Apache Tomcat 9.0 (port 8084) backed by MySQL 8.0 (port 3306) and empirically validated through 15 automated end-to-end functional test cases with a 100.0% pass rate. Observed outcomes demonstrate: zero duplicate reservations under concurrent overlapping date submissions; sub-3-second server boot time; instantaneous price calculation across arbitrary date windows; seamless authentication with zero plaintext password storage via BCrypt salted cryptography; and verified multi-channel simulated payment settlement."),
            # P59: Specific project features linked to SDG
            ("RentRide directly fosters sustainable urban mobility (SDG 11) by offering on-demand shared vehicular access across multiple vehicle classifications (Hatchback, Sedan, SUV, Motorcycle). Centralized fleet inventory and real-time scheduling minimize idle vehicle downtime and maximize asset utilization (SDG 12). The digital booking pipeline and payment sandbox eliminate physical paper contracts and manual bookkeeping (SDG 9), while empowering local rental operators with automated financial tracking and business scalability (SDG 8)."),
            # P61: Measurable or verifiable contribution
            ("Empirically verified across 15 automated test cases, the system optimizes fleet utilization by preventing duplicate booking downtime through pessimistic row locking. Shared vehicle access directly reduces the demand for individual vehicle purchases, curbing urban traffic congestion and vehicular emissions. Furthermore, the 100% digital paperless web workflow eliminates paper rental slips, contracts, and manual receipts, achieving an energy-efficient operational model.")
        ],
        "Minimum 3 objectives ": (
            "• Objective 1: Develop an automated, intuitive self-service portal for browsing, inspecting, and reserving multi-category fleet units.\n"
            "• Objective 2: Enforce strict transactional database concurrency with row-level pessimistic locking (SELECT ... FOR UPDATE) to eliminate double-booking overlaps.\n"
            "• Objective 3: Implement secure authentication via adaptive BCrypt salted password hashing and role-based access control (RBAC).\n"
            "• Objective 4: Build a centralized operational dashboard for real-time KPI metrics, gross revenue calculation, and fleet governance.\n"
            "• Objective 5: Create an interactive mock payment gateway sandbox simulating Credit/Debit Card, UPI, and Netbanking transactions."
        ),
        "Minimum 2 users’ / beneficiaries’ details": (
            "• Individual Customers & Urban Commuters: Commuters, business professionals, and travelers seeking affordable, transparent, on-demand vehicle rentals with instantaneous booking confirmations and personal reservation dashboards.\n"
            "• Fleet Managers & Rental Business Operators: Commercial rental agencies and fleet administrators who gain real-time visibility into vehicle utilization, gross revenue analytics, automated reservation approval, and centralized fleet maintenance."
        )
    }

    # Replace placeholders in paragraphs
    min_3_5_idx = 0
    for p in doc.paragraphs:
        t = p.text.strip()
        if "Minimum 3 to 5 lines required" in t:
            if min_3_5_idx < len(summary_replacements["Minimum 3 to 5 lines required"]):
                rep = summary_replacements["Minimum 3 to 5 lines required"][min_3_5_idx]
                p.text = rep
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(5)
                p.paragraph_format.line_spacing = 1.15
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(9.5)
                min_3_5_idx += 1
        elif "Minimum 3 objectives" in t:
            p.text = summary_replacements["Minimum 3 objectives "]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
        elif "Minimum 2 users" in t:
            p.text = summary_replacements["Minimum 2 users’ / beneficiaries’ details"]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
        elif "Primary SDG:" in t:
            p.text = "Primary SDG: SDG 11 (Sustainable Cities and Communities)    Secondary SDG(s): SDG 8, SDG 9, SDG 12"
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.bold = True
        elif "I, ______________________________________" in t:
            p.text = (
                "I, GUBBALA CHAITANYA SAI KRISHNA, bearing Roll No. 24761A0517, declare that the information "
                "provided in this template accurately describes my work and its relationship to the selected "
                "Programme Outcomes, Programme Specific Outcomes, and Sustainable Development Goals. The SDG "
                "mappings are based on the project’s actual objectives, features, and expected or demonstrated outcomes."
            )
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
        elif "Student Signature(s):" in t:
            p.text = "Student Signature(s): G. Chaitanya Sai Krishna"
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.bold = True
        elif "Date: " in t:
            p.text = "Date: October 26, 2026"
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.bold = True

    # 3. Populate Table 2: Mapping with Programme Outcomes (POs)
    t2 = doc.tables[1]
    po_mappings = [
        ("PO1", "Applied mathematical models for calendar duration and rental pricing calculation (Days * Daily Rate). Leveraged core computer science and software engineering principles in Java 21, object-oriented design patterns (MVC, DAO), and relational database normalization (3NF)."),
        ("PO2", "Formulated solutions for the critical double-booking concurrency challenge in scheduling systems. Analyzed date-interval intersection logic (start_date < ? AND end_date > ?) and implemented pessimistic row locking (SELECT ... FOR UPDATE) to eliminate race conditions."),
        ("PO3", "Architected and implemented a complete Three-Tier enterprise solution meeting customer booking and administrator governance requirements. Designed modular servlet controllers, JDBC DAOs, and responsive JSP presentation views."),
        ("PO4", "Conducted systematic investigations into date overlap collisions and transaction rollbacks. Verified application correctness across 15 comprehensive automated test cases, empirically validating data integrity and session security."),
        ("PO5", "Employed modern software engineering tools including Java 21 LTS OpenJDK, Apache Tomcat 9.0.120, MySQL Community Server 8.0, Selenium WebDriver 4.x with headless Microsoft Edge, and Python test harnesses."),
        ("PO6", "Addressed societal transportation challenges by facilitating the sharing economy, optimizing vehicle utilization to reduce urban traffic congestion, reliance on private car ownership, and environmental pollution."),
        ("PO7", "Enforced professional ethics by protecting user privacy, implementing salted BCrypt password hashing without plaintext storage, preventing privilege escalation via RBAC, and ensuring fully transparent pricing without hidden charges."),
        ("PO8", "Engineered modular software components partitioned into distinct packages (model, dao, controller, util, webapp), establishing clean interfaces and separation of concerns that support multi-developer collaborative engineering."),
        ("PO9", "Generated comprehensive technical documentation, detailed relational schemas, empirical test results, and responsive UI feedback with explicit error messages and validation alerts."),
        ("PO10", "Incorporated financial tracking mechanisms including dynamic rate calculation, multi-method simulated payment processing, and administrator gross revenue aggregation for commercial viability."),
        ("PO11", "Demonstrated self-directed learning and adaptation by mastering modern Java EE servlet specifications, JDBC concurrency locking, modern CSS custom properties, and automated headless browser verification techniques.")
    ]

    for idx, (po_num, desc) in enumerate(po_mappings):
        cell = t2.rows[idx + 1].cells[2]
        format_cell(cell, desc, font_size=9)

    # 4. Populate Table 3: Mapping with Programme Specific Outcomes (PSOs)
    t3 = doc.tables[2]
    pso_mappings = [
        ("PSO1", "Applied standard software engineering practices (MVC architecture, DAO design pattern, thread-safe connection management, unit testing) entirely within an open-source development stack (Java OpenJDK, Apache Tomcat, MySQL Community Edition)."),
        ("PSO2", "Engineered a robust multi-tier web application operating over standard HTTP/1.1 networking protocols, managing session states via secure HTTP cookies, and addressing societal needs for accessible, affordable urban transportation."),
        ("PSO3", "Analyzed, designed, and implemented a normalized relational MySQL database schema (users, vehicles, bookings, payments) with foreign key constraints, cascading referential actions, indexed queries, and row-level pessimistic locking via JDBC.")
    ]

    for idx, (pso_num, desc) in enumerate(pso_mappings):
        cell = t3.rows[idx + 1].cells[1]
        format_cell(cell, desc, font_size=9)

    # 5. Populate Table 4: Mapping with Sustainable Development Goals (SDGs)
    t4 = doc.tables[3]
    sdg_mappings = {
        8: ("Decent Work and Economic Growth", "Enables local car rental agencies and fleet owners to digitize their business operations, improve operational efficiency, automate bookkeeping, and expand their economic reach through digital commerce channels."),
        9: ("Industry, Innovation and Infrastructure", "Modernizes traditional transportation services through innovative digital infrastructure, open-source enterprise architecture, and real-time database-driven reservation technology."),
        11: ("Sustainable Cities and Communities", "Promotes sustainable urban shared mobility by optimizing the utility and occupancy of shared vehicle fleets, thereby reducing the demand for personal vehicle ownership, minimizing traffic congestion, and curbing vehicular exhaust emissions. (Primary SDG)"),
        12: ("Responsible Consumption and Production", "Fosters the circular and sharing economy by maximizing the operational lifecycle of vehicles through shared access rather than manufacturing excess private vehicles, minimizing resource consumption and automotive waste.")
    }

    for row_idx in range(1, 18):
        sdg_num = row_idx # 1 to 17
        chk_cell = t4.rows[row_idx].cells[0]
        desc_cell = t4.rows[row_idx].cells[3]

        if sdg_num in sdg_mappings:
            chk_cell.text = "☑" # Checked box
            p_chk = chk_cell.paragraphs[0]
            p_chk.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p_chk.runs:
                r.font.name = "Segoe UI Symbol"
                r.font.size = Pt(11)
                r.font.bold = True
                r.font.color.rgb = RGBColor(5, 150, 105) # Emerald Green

            goal_title, reason = sdg_mappings[sdg_num]
            format_cell(desc_cell, reason, font_size=8.5)
        else:
            chk_cell.text = "☐" # Unchecked box
            p_chk = chk_cell.paragraphs[0]
            p_chk.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p_chk.runs:
                r.font.name = "Segoe UI Symbol"
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(148, 163, 184)
            desc_cell.text = "—"
            p_d = desc_cell.paragraphs[0]
            p_d.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p_d.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.color.rgb = RGBColor(148, 163, 184)

    # Save filled document
    doc.save(OUTPUT_DOCX)
    print(f"Successfully generated populated document: {OUTPUT_DOCX}")

if __name__ == "__main__":
    populate_alignment_document()
