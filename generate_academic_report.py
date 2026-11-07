# -*- coding: utf-8 -*-
"""
Script to generate the complete academic project report for:
VEHICLE RENTAL SYSTEM (RentRide)
Student: GUBBALA CHAITANYA SAI KRISHNA (24761A0517)
College: Lakireddy Bali Reddy College of Engineering (Autonomous)
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def create_element(name):
    return OxmlElement(name)

def set_cell_border(cell, **kwargs):
    """
    Set cell borders
    kwargs: top, bottom, left, right
    values: dict(sz=12, val='single', color='000000', space='0')
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                          r'<w:top w:val="none"/>'
                          r'<w:left w:val="none"/>'
                          r'<w:bottom w:val="none"/>'
                          r'<w:right w:val="none"/>'
                          r'</w:tcBorders>')
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = tcBorders.find(qn(tag))
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', 'CCCCCC'))
    tcPr.append(tcBorders)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def build_report():
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)

    # Base styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0, 0, 0)

    logo_path = 'lbrce_logo.jpeg'

    # =========================================================================
    # 1. TITLE / COVER PAGE
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("VEHICLE RENTAL SYSTEM\n(RentRide)")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(20)
    run.font.bold = True
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("A\nSkill Oriented Course Web Application / Project Report\nsubmitted in partial fulfillment of the requirements for the award of the Degree of")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.italic = True
    p.paragraph_format.space_after = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("BACHELOR OF TECHNOLOGY\nIN\nCOMPUTER SCIENCE AND ENGINEERING")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    p.paragraph_format.space_after = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("By")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("GUBBALA CHAITANYA SAI KRISHNA\n(Regd. No: 24761A0517)")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.font.bold = True
    p.paragraph_format.space_after = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Under the esteemed guidance of\n")
    run.font.size = Pt(11)
    run.font.italic = True
    run2 = p.add_run("Dr. K. DeviPriya, M.Tech., Ph.D.\n")
    run2.font.size = Pt(13)
    run2.font.bold = True
    run3 = p.add_run("Professor, Department of CSE")
    run3.font.size = Pt(11)
    p.paragraph_format.space_after = Pt(12)

    if os.path.exists(logo_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(8)
        p_img.add_run().add_picture(logo_path, width=Inches(1.3))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n"
                    "LAKIREDDY BALIREDDY COLLEGE OF ENGINEERING (AUTONOMOUS)\n")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run_sub = p.add_run("Accredited by NAAC with 'A' Grade & NBA (Under Tier - I)\n"
                        "An ISO 21001:2018, 14001:2015, 50001:2018 Certified Institution\n"
                        "Approved by AICTE, New Delhi and Affiliated to JNTUK, Kakinada\n"
                        "L.B. REDDY NAGAR, MYLAVARAM, NTR DIST., A.P. - 521230\n"
                        "2024–2028")
    run_sub.font.name = 'Times New Roman'
    run_sub.font.size = Pt(9.5)
    p.paragraph_format.space_after = Pt(0)

    doc.add_page_break()

    # =========================================================================
    # 2. CERTIFICATE PAGE
    # =========================================================================
    if os.path.exists(logo_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(logo_path, width=Inches(1.1))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run("LAKIREDDY BALI REDDY COLLEGE OF ENGINEERING (AUTONOMOUS)\n")
    r1.font.bold = True
    r1.font.size = Pt(12)
    r2 = p.add_run("Accredited by NAAC with 'A' Grade & NBA (Under Tier - I)\n"
                   "An ISO 21001:2018, 14001:2015, 50001:2018 Certified Institution\n"
                   "Approved by AICTE, New Delhi and Affiliated to JNTUK, Kakinada\n"
                   "L.B. REDDY NAGAR, MYLAVARAM, NTR DIST., A.P. - 521230\n")
    r2.font.size = Pt(9.5)
    r3 = p.add_run("Department of\nCOMPUTER SCIENCE AND ENGINEERING\n")
    r3.font.bold = True
    r3.font.size = Pt(11)
    p.paragraph_format.space_after = Pt(12)

    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cert = p_cert.add_run("CERTIFICATE")
    r_cert.font.bold = True
    r_cert.font.size = Pt(15)
    r_cert.underline = True
    p_cert.paragraph_format.space_after = Pt(14)

    p_body = doc.add_paragraph()
    p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_body.paragraph_format.line_spacing = 1.5
    p_body.paragraph_format.space_after = Pt(12)
    p_body.add_run(
        "This is to certify that the Skill Oriented Course Web Application / Project report entitled "
        "“VEHICLE RENTAL SYSTEM (RentRide)” is being submitted by GUBBALA CHAITANYA SAI KRISHNA (Regd. No: 24761A0517) "
        "in partial fulfillment of the requirements for the award of degree of Bachelor of Technology in "
        "Computer Science and Engineering from Jawaharlal Nehru Technological University Kakinada is a record of "
        "bonafide work carried out by him at Lakireddy Bali Reddy College of Engineering (Autonomous).\n\n"
        "The results embodied in this Skill Oriented Course Web Application / Project report have not been submitted "
        "to any other university or institute for the award of any degree or diploma."
    )

    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(30)
    p_sign.paragraph_format.space_after = Pt(36)
    r_g = p_sign.add_run("PROJECT GUIDE                                                                         HEAD OF THE DEPARTMENT\n")
    r_g.font.bold = True
    r_g_sub = p_sign.add_run("Dr. K. DeviPriya, M.Tech., Ph.D.                                                Dr. S. Nagarjuna Reddy, M.Tech., Ph.D.\n"
                             "Professor, Dept. of CSE                                                                Professor & HOD, Dept. of CSE")
    r_g_sub.font.size = Pt(10)

    # Examiner Table
    table_ex = doc.add_table(rows=1, cols=2)
    table_ex.alignment = WD_TABLE_ALIGNMENT.CENTER
    row = table_ex.rows[0]
    c1, c2 = row.cells[0], row.cells[1]
    c1.width = Inches(3.2)
    c2.width = Inches(3.2)
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p1.add_run("INTERNAL EXAMINER").font.bold = True
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.add_run("EXTERNAL EXAMINER").font.bold = True

    doc.add_page_break()

    # =========================================================================
    # 3. ACKNOWLEDGEMENT PAGE
    # =========================================================================
    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ack = p_ack.add_run("ACKNOWLEDGEMENT")
    r_ack.font.bold = True
    r_ack.font.size = Pt(15)
    r_ack.underline = True
    p_ack.paragraph_format.space_after = Pt(16)

    ack_texts = [
        "I would like to express my sincere gratitude and deep sense of indebtedness to my project guide Dr. K. DeviPriya, Professor, Department of Computer Science and Engineering, for her invaluable guidance, encouragement, constructive suggestions, and continuous support throughout the development of this Skill Oriented Course Web Application / Project.",
        "I also take this privilege to record my profound thanks to Dr. S. Nagarjuna Reddy, Professor and Head of the Department of CSE, whose valuable support, encouragement, and cooperative academic environment crowned this project with success.",
        "I express my humble thanks to the College Management for providing state-of-the-art laboratory facilities and computing infrastructure. I also express my sincere gratitude and deep sense of respect to Dr. K. Appa Rao, Principal, for making all required assistance available and for his inspiring leadership in carrying out this project in the Institute.",
        "I am deeply thankful to the faculty members and non-teaching staff of the Department of Computer Science and Engineering for their direct and indirect assistance and cooperation during the progression of this project.",
        "Finally, I am elated to avail myself of this opportunity to express my deepest gratitude and love to my parents and friends for their moral encouragement, patience, and unstinted blessings throughout my academic journey."
    ]

    for t in ack_texts:
        p_t = doc.add_paragraph()
        p_t.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_t.paragraph_format.line_spacing = 1.5
        p_t.paragraph_format.space_after = Pt(10)
        p_t.add_run(t)

    p_stu = doc.add_paragraph()
    p_stu.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_stu.paragraph_format.space_before = Pt(24)
    r_s = p_stu.add_run("GUBBALA CHAITANYA SAI KRISHNA\n(Regd. No: 24761A0517)\nB.Tech - Computer Science and Engineering")
    r_s.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # 4. DECLARATION PAGE
    # =========================================================================
    p_dec = doc.add_paragraph()
    p_dec.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dec = p_dec.add_run("DECLARATION")
    r_dec.font.bold = True
    r_dec.font.size = Pt(15)
    r_dec.underline = True
    p_dec.paragraph_format.space_after = Pt(16)

    p_dtext = doc.add_paragraph()
    p_dtext.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dtext.paragraph_format.line_spacing = 1.5
    p_dtext.paragraph_format.space_after = Pt(14)
    p_dtext.add_run(
        "I hereby declare that the Skill Oriented Course Web Application / Project report entitled "
        "“VEHICLE RENTAL SYSTEM (RentRide)” submitted by me in partial fulfillment of the requirements for "
        "the award of the degree of Bachelor of Technology in Computer Science and Engineering to Lakireddy "
        "Bali Reddy College of Engineering (Autonomous), affiliated to JNTUK Kakinada, is a bonafide record of "
        "original work carried out by me under the supervision and guidance of Dr. K. DeviPriya, Professor, "
        "Department of Computer Science and Engineering.\n\n"
        "I certify that the work contained in this report is original and has not been submitted to any other "
        "institute or university for the award of any degree or diploma. I have confirmed with the norms and "
        "guidelines stipulated in the Ethical Code of Conduct of the Institute. Whenever materials (code patterns, "
        "literature, or concepts) have been taken from other sources, due credit has been given by citing them "
        "appropriately in the text and references."
    )

    p_dsign = doc.add_paragraph()
    p_dsign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_dsign.paragraph_format.space_before = Pt(40)
    p_dsign.add_run("Signature of the Student\n\n\n").font.bold = True
    r_ds = p_dsign.add_run("GUBBALA CHAITANYA SAI KRISHNA\nRegd. No: 24761A0517")
    r_ds.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # 5. ABSTRACT
    # =========================================================================
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_abs = p_abs.add_run("ABSTRACT")
    r_abs.font.bold = True
    r_abs.font.size = Pt(15)
    r_abs.underline = True
    p_abs.paragraph_format.space_after = Pt(14)

    p_atext = doc.add_paragraph()
    p_atext.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_atext.paragraph_format.line_spacing = 1.5
    p_atext.paragraph_format.space_after = Pt(12)
    p_atext.add_run(
        "Modern urban mobility demands efficient, transparent, and scalable vehicle rental solutions that "
        "eliminate the inefficiencies, scheduling collisions, and paper-based tracking inherent in traditional manual systems. "
        "This project presents “RentRide” (Vehicle Rental System), an enterprise-ready, full-stack web application developed "
        "using Java EE architecture (Servlets 4.0, JavaServer Pages 2.3, JDBC) and a relational MySQL database server.\n\n"
        "The system incorporates a robust Model-View-Controller (MVC) architectural pattern, cleanly separating presentation "
        "interfaces, controller request orchestration, and data access objects. A core technical highlight is its transactional "
        "concurrency management engine: utilizing database-level pessimistic row-locking (`SELECT ... FOR UPDATE`) and rigorous "
        "date overlap validation algorithms, the platform guarantees zero double-booking occurrences even under high concurrent load. "
        "Security is fortified using the industry-standard jBCrypt library for salted cryptographic password hashing, along with "
        "session-fixation mitigation protocols and HttpOnly session cookies.\n\n"
        "The frontend provides an interactive, responsive user experience built with modern CSS custom variables and dynamic "
        "client-side rental tariff calculation scripts. RentRide offers a dual-role ecosystem: authenticated customers can browse "
        "categorized vehicle fleets (Hatchback, Sedan, SUV, Bike), review detailed vehicle specifications, reserve multi-day windows, "
        "simulate multi-channel payments (Card, UPI, Net Banking) via a safe mock sandbox, and monitor their active reservations. "
        "Concurrently, the administrative portal provides real-time operational analytics, revenue metrics, complete fleet inventory "
        "management (CRUD), and reservation approval workflows. The system has been validated through an automated Python end-to-end "
        "regression test suite, verifying functional correctness, access control, and edge-case concurrency handling across all modules."
    )

    doc.add_page_break()

    # =========================================================================
    # 6. TABLE OF CONTENTS
    # =========================================================================
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_toc = p_toc.add_run("LIST OF CONTENTS")
    r_toc.font.bold = True
    r_toc.font.size = Pt(15)
    r_toc.underline = True
    p_toc.paragraph_format.space_after = Pt(14)

    toc_items = [
        ("1. INTRODUCTION", "1"),
        ("   1.1 Overview of the Project", "1"),
        ("   1.2 Problem Statement", "2"),
        ("   1.3 Existing System & Limitations", "2"),
        ("   1.4 Proposed System & Innovations", "3"),
        ("   1.5 Objectives and Scope of the Project", "4"),
        ("   1.6 Feasibility Study (Technical, Operational, Economic)", "5"),
        ("2. TECHNOLOGIES USED & REQUIREMENTS", "7"),
        ("   2.1 HTML5, CSS3 & JavaScript", "7"),
        ("   2.2 Java Platform & Apache Tomcat 9.0", "9"),
        ("   2.3 Java Database Connectivity (JDBC) & MySQL Connector", "11"),
        ("   2.4 Java Servlets Architecture & Lifecycle", "13"),
        ("   2.5 JavaServer Pages (JSP) & Expression Language", "15"),
        ("   2.6 MySQL Relational Database Management System", "17"),
        ("   2.7 jBCrypt Cryptographic Security", "19"),
        ("   2.8 Hardware and Software Requirements", "20"),
        ("3. WEB APPLICATION ARCHITECTURE & SYSTEM DESIGN", "21"),
        ("   3.1 3-Tier MVC Architectural Design", "21"),
        ("   3.2 System Modules Description (Customer & Admin)", "22"),
        ("   3.3 Database Design & E-R Diagram", "24"),
        ("   3.4 Data Flow Diagrams (Level 0, Level 1, Level 2)", "26"),
        ("   3.5 UML Diagrams (Use Case, Sequence, Class)", "28"),
        ("4. CODING & IMPLEMENTATION", "30"),
        ("   4.1 Database Scripts (schema.sql)", "30"),
        ("   4.2 Database Utility Layer (DBConnection.java)", "31"),
        ("   4.3 Model Entities (User, Vehicle, Booking, Payment)", "32"),
        ("   4.4 Data Access Layer (DAOs Implementation)", "34"),
        ("   4.5 Servlet Controllers & URL Routing", "38"),
        ("   4.6 Concurrency & Pessimistic Locking Implementation", "41"),
        ("   4.7 Security & Session Management Implementation", "43"),
        ("5. USER INTERFACE & SCREENS", "45"),
        ("   5.1 Customer Interface Walkthrough", "45"),
        ("   5.2 Administrator Dashboard & Controls", "48"),
        ("6. TESTING & VALIDATION", "51"),
        ("   6.1 Testing Methodology & Objectives", "51"),
        ("   6.2 Automated Python Test Suite (test_rental_system.py)", "52"),
        ("   6.3 Comprehensive Test Cases & Results Matrix", "53"),
        ("   6.4 Concurrency & Edge-Case Validation", "55"),
        ("7. CONCLUSION & FUTURE ENHANCEMENTS", "56"),
        ("   7.1 Conclusion", "56"),
        ("   7.2 Future Enhancements", "57"),
        ("REFERENCES", "58"),
        ("LIST OF ABBREVIATIONS", "59")
    ]

    t_toc = doc.add_table(rows=1, cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t_toc.rows[0]
    hdr.cells[0].paragraphs[0].add_run("CONTENTS").font.bold = True
    hdr.cells[1].paragraphs[0].add_run("PAGE NO").font.bold = True
    hdr.cells[0].width = Inches(5.2)
    hdr.cells[1].width = Inches(1.2)
    hdr.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_cell_shading(hdr.cells[0], "F1F5F9")
    set_cell_shading(hdr.cells[1], "F1F5F9")

    for title, pg in toc_items:
        row = t_toc.add_row()
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.2)
        c1.width = Inches(1.2)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = p0.add_run(title)
        if title.startswith("1.") or title.startswith("2.") or title.startswith("3.") or title.startswith("4.") or title.startswith("5.") or title.startswith("6.") or title.startswith("7.") or "REFERENCES" in title or "ABBREVIATIONS" in title:
            r.font.bold = True
        p1.add_run(pg)
        set_cell_border(c0, bottom=dict(sz=2, val='single', color='E2E8F0'))
        set_cell_border(c1, bottom=dict(sz=2, val='single', color='E2E8F0'))

    doc.add_page_break()

    # =========================================================================
    # 7. LIST OF ABBREVIATIONS
    # =========================================================================
    p_abb = doc.add_paragraph()
    p_abb.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_abb = p_abb.add_run("LIST OF ABBREVIATIONS")
    r_abb.font.bold = True
    r_abb.font.size = Pt(15)
    r_abb.underline = True
    p_abb.paragraph_format.space_after = Pt(14)

    abbreviations = [
        ("HTML", "HyperText Markup Language"),
        ("CSS", "Cascading Style Sheets"),
        ("JS", "JavaScript"),
        ("JSP", "JavaServer Pages"),
        ("JDBC", "Java Database Connectivity"),
        ("SQL", "Structured Query Language"),
        ("RDBMS", "Relational Database Management System"),
        ("MVC", "Model-View-Controller"),
        ("DAO", "Data Access Object"),
        ("POJO", "Plain Old Java Object"),
        ("API", "Application Programming Interface"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("HTTPS", "Hypertext Transfer Protocol Secure"),
        ("URI / URL", "Uniform Resource Identifier / Uniform Resource Locator"),
        ("RBAC", "Role-Based Access Control"),
        ("DFD", "Data Flow Diagram"),
        ("ERD", "Entity-Relationship Diagram"),
        ("UML", "Unified Modeling Language"),
        ("XSS", "Cross-Site Scripting"),
        ("CRUD", "Create, Read, Update, Delete"),
        ("LTS", "Long Term Support"),
        ("WAR", "Web Application Archive")
    ]

    t_abb = doc.add_table(rows=1, cols=2)
    t_abb.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_abb = t_abb.rows[0]
    h_abb.cells[0].paragraphs[0].add_run("Abbreviation").font.bold = True
    h_abb.cells[1].paragraphs[0].add_run("Expansion / Description").font.bold = True
    h_abb.cells[0].width = Inches(2.2)
    h_abb.cells[1].width = Inches(4.2)
    set_cell_shading(h_abb.cells[0], "F1F5F9")
    set_cell_shading(h_abb.cells[1], "F1F5F9")

    for a, desc in abbreviations:
        row = t_abb.add_row()
        row.cells[0].width = Inches(2.2)
        row.cells[1].width = Inches(4.2)
        row.cells[0].paragraphs[0].add_run(a).font.bold = True
        row.cells[1].paragraphs[0].add_run(desc)
        set_cell_border(row.cells[0], bottom=dict(sz=2, val='single', color='E2E8F0'))
        set_cell_border(row.cells[1], bottom=dict(sz=2, val='single', color='E2E8F0'))

    doc.add_page_break()

    # Helper function to add chapter headings
    def add_chapter_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(f"CHAPTER {num_str}\n{title_str.upper()}")
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_section_heading(sec_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(sec_str)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(37, 99, 235)
        return p

    def add_body_p(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(8)
        p.add_run(text)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(4)
        r_pre = p.add_run(bold_prefix + " ")
        r_pre.font.bold = True
        p.add_run(text)
        return p

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_chapter_heading("1", "INTRODUCTION")

    add_section_heading("1.1 Overview of the Project")
    add_body_p(
        "In the contemporary landscape of travel and urban transportation, vehicle rental services have become indispensable. "
        "Whether for daily business commutes, weekend tourism, family vacations, or short-term emergency transit, consumers seek "
        "convenient, accessible, and dependable personal mobility without the significant capital and depreciation overhead of vehicle ownership. "
        "“RentRide” (Vehicle Rental System) is a comprehensive web-based enterprise solution engineered to bridge the divide between vehicle rental operators "
        "and modern travelers."
    )
    add_body_p(
        "Built on the proven Java EE ecosystem utilizing Java Servlets 4.0, JavaServer Pages (JSP 2.3), and Java Database Connectivity (JDBC) "
        "interfacing with a robust MySQL 8.0 relational database engine, RentRide automates the entire vehicle rental lifecycle. The system provides "
        "customers with self-service fleet exploration, transparent pricing calculations, instant reservations, conflict-free scheduling, "
        "and a realistic payment simulation sandbox. Concurrently, it empowers fleet administrators with centralized inventory controls, real-time "
        "revenue metrics, and reservation management capabilities."
    )

    add_section_heading("1.2 Problem Statement")
    add_body_p(
        "Traditional vehicle rental businesses continue to struggle with disjointed, manual, or semi-automated processes. "
        "Key operational challenges in conventional systems include:"
    )
    add_bullet("Double-Booking Collisions:", "Without synchronized atomic locking mechanisms, concurrent reservations frequently assign the same vehicle to different clients for overlapping dates, causing customer frustration and brand damage.")
    add_bullet("Opaque Pricing Structures:", "Manual paper quotes often conceal extra tariffs, driver fees, and arbitrary weekend surcharges, leaving customers distrustful.")
    add_bullet("Manual Administrative Burden:", "Fleet managers spend excessive time checking paper logbooks and spreadsheets to verify vehicle availability, maintenance status, and payment clearances.")
    add_bullet("Security & Data Integrity Risks:", "Customer credentials and rental records stored insecurely or in plaintext expose organizations to identity theft and regulatory non-compliance.")

    add_section_heading("1.3 Existing System & Its Limitations")
    add_body_p(
        "In existing manual or legacy desktop rental systems, a prospective customer must physically visit a rental counter or make inquiries via telephone. "
        "The operator consults a physical logbook to check vehicle availability, manually tallies the rental duration, writes handwritten paper invoices, "
        "and collects physical cash or unsynchronized card payments."
    )
    add_body_p("Major limitations of the existing system comprise:")
    add_bullet("High Latency & Queuing:", "Customers face substantial waiting times for availability checks and paper documentation.")
    add_bullet("Human Calculation Errors:", "Manual tariff calculations frequently introduce arithmetic errors in multi-day rentals.")
    add_bullet("Lack of Real-Time Analytics:", "Business owners have no instant visibility into daily revenue, active fleet capacity, or cancellation frequencies.")
    add_bullet("Limited Geographical Reach:", "Operations are constrained strictly to business hours and physical counter locations.")

    add_section_heading("1.4 Proposed System & Key Innovations")
    add_body_p(
        "The proposed RentRide web application transforms these manual operations into a cloud-ready, responsive, automated web portal. "
        "Key architectural and functional innovations include:"
    )
    add_bullet("Self-Service Digital Catalog:", "Real-time fleet directory organized into Hatchback, Sedan, SUV, and Motorcycle categories with authentic vehicle photography and transparent daily tariffs.")
    add_bullet("Pessimistic Concurrency Locking:", "Utilizes database-level `SELECT ... FOR UPDATE` row locks combined with chronological SQL date overlap queries (`start_date < ? AND end_date > ?`) to mathematically eliminate double-booking.")
    add_bullet("Automated Tariff Engine:", "Instant JavaScript-driven cost projection on the client side combined with robust server-side `ChronoUnit.DAYS` billing calculation.")
    add_bullet("Enterprise-Grade Cryptography:", "Integration of the jBCrypt cryptographic library using salted BCrypt hashing (`$2a$10$...`) to ensure complete protection of user credentials.")
    add_bullet("Role-Based Management Portal:", "Segregated, password-protected administrative interfaces providing real-time KPI metrics, gross revenue analytics, and instant fleet status toggles.")

    add_section_heading("1.5 Objectives and Scope of the Project")
    add_body_p(
        "The core objective of RentRide is to develop a reliable, secure, user-centric, and scalable vehicle rental web application. "
        "Specific objectives include:"
    )
    add_bullet("1.", "To architect an intuitive online portal allowing customers to browse and book vehicles 24/7.")
    add_bullet("2.", "To enforce strict transactional integrity and prevent overlapping bookings through atomic database transactions.")
    add_bullet("3.", "To implement a simulated payment gateway sandbox (supporting mock Card, UPI, and Net Banking) for risk-free checkout demonstration.")
    add_bullet("4.", "To provide administrators with real-time operational oversight including gross revenue calculation, fleet inventory CRUD, and reservation moderation.")
    add_bullet("5.", "To build a robust, maintainable codebase following the 3-Tier MVC architectural standard.")

    add_body_p(
        "Scope: The scope encompasses user account management, session security, dynamic vehicle cataloging, multi-day reservation processing, "
        "conflict prevention, mock payment settlement, customer booking history, and comprehensive admin controls. "
        "External hardware telemetry (GPS tracking) and live commercial banking payment webhooks remain outside the current project scope."
    )

    add_section_heading("1.6 Feasibility Study")
    add_body_p(
        "Prior to development, a thorough feasibility study was conducted across technical, operational, and economic dimensions:"
    )
    add_bullet("1.6.1 Technical Feasibility:", "The project utilizes mature, industry-standard technologies (Java 21, Apache Tomcat 9, MySQL 8.0, and modern web standards). The development environment (Eclipse IDE, Antigravity IDE) and hardware infrastructure easily satisfy the runtime and compilation requirements. The open architecture of Java EE ensures straightforward maintenance and modular enhancement.")
    add_bullet("1.6.2 Operational Feasibility:", "The user interface is designed with a high level of aesthetic polish, clear visual hierarchy, and intuitive navigation. Users require no specialized training to browse vehicles, select dates, and complete simulated checkouts. Administrative controls feature responsive data tables, status toggles, and modal dialogues that streamline fleet oversight.")
    add_bullet("1.6.3 Economic Feasibility:", "The entire technology stack consists of open-source and freely available software tools (Java OpenJDK, Apache Tomcat, MySQL Community Server, jBCrypt, Python). No costly proprietary software licenses or runtime royalties are incurred, making the system exceptionally cost-effective to develop, deploy, and maintain.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: TECHNOLOGIES USED & REQUIREMENTS
    # =========================================================================
    add_chapter_heading("2", "TECHNOLOGIES USED & SYSTEM REQUIREMENTS")

    add_section_heading("2.1 HTML5, CSS3 & JavaScript")
    add_body_p(
        "The presentation tier of RentRide is engineered using standard HTML5 semantic elements, custom modern CSS3, and lightweight vanilla JavaScript ES6. "
        "The user experience emphasizes clean visual hierarchy, crisp typography, and responsive layouts."
    )
    add_bullet("HTML5 Semantic Structure:", "Pages employ semantic tags such as `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, and `<footer>` to guarantee optimal document outline, accessibility, and SEO readiness.")
    add_bullet("Custom CSS3 Design System (`style.css`):", "A complete design system is implemented using CSS custom properties (`:root` variables) defining primary palettes (`#2563eb`), dark slate backgrounds (`#0f172a`), functional status colors (success, warning, danger), subtle box shadows, rounded borders (`var(--radius-md)`), and responsive grid systems (`.vehicle-grid`, `.metrics-grid`).")
    add_bullet("Client-Side Dynamic JavaScript:", "On the booking interface (`booking.jsp`), interactive JavaScript monitors the Pick-up and Drop-off date inputs, automatically sets the minimum permissible drop-off date, computes the difference in rental days, and renders an instant estimated cost breakdown without requiring full page roundtrips.")

    add_section_heading("2.2 Java Platform & Apache Tomcat 9.0")
    add_body_p(
        "The server-side business logic and controller orchestration run on the Java Platform, Standard Edition 21 (JavaSE-21 LTS), "
        "hosted within the Apache Tomcat v9.0 web application container."
    )
    add_bullet("JavaSE-21 LTS:", "Provides modern language features, high-performance garbage collection, strong type safety, and robust date-time arithmetic via the `java.time` package (e.g., `ChronoUnit.DAYS` and `LocalDate`).")
    add_bullet("Apache Tomcat v9.0:", "A high-performance, open-source servlet container implementing Java Servlet 4.0 and JavaServer Pages (JSP) 2.3 specifications. Tomcat manages HTTP connector threads, session persistence, and servlet lifecycle execution.")

    add_section_heading("2.3 Java Database Connectivity (JDBC) & MySQL Connector/J")
    add_body_p(
        "Data persistence and relational communication are mediated through Java Database Connectivity (JDBC). "
        "The project utilizes the official MySQL Connector/J driver (`mysql-connector-j-26.7.0.jar`, class `com.mysql.cj.jdbc.Driver`)."
    )
    add_body_p(
        "A centralized utility class, `DBConnection.java`, manages JDBC connection lifecycles. All database operations strictly employ "
        "`PreparedStatement` interfaces. Parameterized queries bind values at runtime, preventing SQL injection vulnerabilities. "
        "Furthermore, multi-step operations (such as booking creation and payment settlement) utilize explicit JDBC transaction control (`con.setAutoCommit(false)`, `con.commit()`, and `con.rollback()`)."
    )

    add_section_heading("2.4 Java Servlets Architecture & Lifecycle")
    add_body_p(
        "Java Servlets serve as the foundational controllers within RentRide's MVC architecture. All servlets are declared using modern "
        "`@WebServlet` annotations, eliminating verbose XML configuration."
    )
    add_body_p(
        "During execution, each incoming HTTP request triggers the servlet container to invoke the servlet's `service()` method, which routes "
        "the request to `doGet()` or `doPost()`. The servlets extract and sanitize request parameters, enforce session and role authorizations, "
        "invoke the corresponding DAO business methods, populate request attributes (`request.setAttribute()`), and dispatch responses to JSP views "
        "via `RequestDispatcher.forward()` or send client redirects via `response.sendRedirect()`."
    )

    add_section_heading("2.5 JavaServer Pages (JSP) & Expression Language (EL)")
    add_body_p(
        "JavaServer Pages technology is leveraged to generate dynamic HTML responses. Key aspects include:"
    )
    add_bullet("JSP Directives:", "`<%@ page contentType=\"text/html;charset=UTF-8\" language=\"java\" %>` ensures uniform UTF-8 character encoding across all views.")
    add_bullet("Modular Component Inclusion:", "`<%@ include file=\"includes/navbar.jsp\" %>` encapsulates navigation header rendering into a single reusable component, ensuring site-wide consistency and zero code duplication.")
    add_bullet("Expression Language (EL):", "Syntax such as `${pageContext.request.contextPath}` ensures context-path-safe hyperlinks and static asset resolution across all deployment environments.")

    add_section_heading("2.6 MySQL Relational Database Management System")
    add_body_p(
        "The relational database tier is powered by MySQL Server 8.0+. The database schema, named `rental_vehicle`, comprises 4 highly normalized tables: "
        "`users`, `vehicles`, `bookings`, and `payments`. Integrity is enforced through primary keys with `AUTO_INCREMENT`, unique keys on vehicle registration numbers and user emails, "
        "and foreign key constraints with `ON DELETE CASCADE` referential actions."
    )

    add_section_heading("2.7 jBCrypt Cryptographic Security")
    add_body_p(
        "User authentication security is powered by the `jBCrypt` library (v0.4, `org.mindrot.jbcrypt.BCrypt`). "
        "During user registration in `RegisterServlet`, passwords are encrypted using a 10-round cryptographic salt: "
        "`BCrypt.hashpw(password, BCrypt.gensalt())`. When authenticating in `LoginServlet`, verification is performed via `BCrypt.checkpw(password, user.getPassword())`. "
        "This ensures that even if database records were compromised, user passwords cannot be decrypted or cracked using rainbow tables."
    )

    add_section_heading("2.8 Hardware and Software Requirements")
    
    # Requirements Table
    t_req = doc.add_table(rows=1, cols=2)
    t_req.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_r = t_req.rows[0]
    h_r.cells[0].paragraphs[0].add_run("Component / Parameter").font.bold = True
    h_r.cells[1].paragraphs[0].add_run("Specification / Environment").font.bold = True
    h_r.cells[0].width = Inches(2.5)
    h_r.cells[1].width = Inches(3.9)
    set_cell_shading(h_r.cells[0], "F1F5F9")
    set_cell_shading(h_r.cells[1], "F1F5F9")

    req_data = [
        ("Operating System", "Windows 10 / 11, Linux (Ubuntu 20.04+), macOS"),
        ("Java Development Kit (JDK)", "JDK 21 LTS (Oracle OpenJDK / Eclipse Temurin)"),
        ("Web Application Server", "Apache Tomcat v9.0.x (Servlet 4.0 / JSP 2.3)"),
        ("Database Management System", "MySQL Server 8.0.x Community Edition"),
        ("JDBC Driver Library", "MySQL Connector/J 26.7.0 (`com.mysql.cj.jdbc.Driver`)"),
        ("Security / Hashing Library", "jBCrypt v0.4 (`org.mindrot.jbcrypt.BCrypt`)"),
        ("Integrated Development Environment", "Eclipse IDE for Enterprise Java & Web Developers"),
        ("Automated Test Framework", "Python 3.10+ (`urllib.request`, `http.cookiejar`)"),
        ("Web Browser", "Google Chrome, Mozilla Firefox, Microsoft Edge"),
        ("System Processor (Hardware)", "Intel Core i3 / AMD Ryzen 3 or higher (2.0 GHz min)"),
        ("RAM / Memory (Hardware)", "8 GB RAM recommended (4 GB minimum)"),
        ("Hard Disk Storage (Hardware)", "500 MB free space for code, server & database files")
    ]

    for k, v in req_data:
        r = t_req.add_row()
        r.cells[0].width = Inches(2.5)
        r.cells[1].width = Inches(3.9)
        r.cells[0].paragraphs[0].add_run(k).font.bold = True
        r.cells[1].paragraphs[0].add_run(v)
        set_cell_border(r.cells[0], bottom=dict(sz=2, val='single', color='E2E8F0'))
        set_cell_border(r.cells[1], bottom=dict(sz=2, val='single', color='E2E8F0'))

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: WEB APPLICATION ARCHITECTURE & SYSTEM DESIGN
    # =========================================================================
    add_chapter_heading("3", "WEB APPLICATION ARCHITECTURE & SYSTEM DESIGN")

    add_section_heading("3.1 3-Tier MVC Architectural Design")
    add_body_p(
        "RentRide is structured around a classic 3-Tier Model-View-Controller (MVC) architecture, establishing strict separation of concerns, "
        "high cohesion, and low coupling:"
    )
    add_bullet("1. Presentation Tier (View):", "Constructed using JSP, HTML5, CSS3, and JavaScript. Responsible solely for displaying data to the user, capturing input, and submitting HTTP GET/POST requests. Includes reusable components such as `navbar.jsp`.")
    add_bullet("2. Business & Controller Tier (Controller & Model):", "Java Servlets intercept incoming HTTP requests, enforce security permissions, and coordinate with the business data layer. Domain model POJOs (`User`, `Vehicle`, `Booking`, `Payment`) represent business entities and data transfer objects (DTOs).")
    add_bullet("3. Data Access & Persistence Tier (DAO & Database):", "Data Access Objects (`UserDAO`, `VehicleDAO`, `BookingDAO`, `PaymentDAO`) encapsulate all JDBC SQL logic, connection handling, and transaction boundaries. The MySQL relational database stores persistent records.")

    add_section_heading("3.2 System Modules Description")
    add_body_p("The system is bifurcated into two primary operational modules based on user roles:")
    add_bullet("3.2.1 Customer Portal (`USER` Role):", 
               "• Account Registration & Login: Secure onboarding with BCrypt encryption.\n"
               "• Fleet Catalog & Details: Browsing categorized vehicles with real photographs and daily prices.\n"
               "• Reservation Engine: Selecting pickup and drop-off dates with instant price projection.\n"
               "• Mock Payment Sandbox: Simulating Card, UPI, or Net Banking authorizations.\n"
               "• My Bookings Dashboard: Reviewing reservation histories, completing pending payments, and cancelling active bookings.")
    add_bullet("3.2.2 Staff & Administrator Portal (`ADMIN` Role):", 
               "• Operational Analytics Dashboard: Real-time metrics for total fleet units, active units, total bookings, pending approvals, and gross settled revenue.\n"
               "• Fleet Inventory Management: Full CRUD operations for vehicle records, including registration number, make, model, category, rate, and status toggles (`AVAILABLE` / `UNAVAILABLE`).\n"
               "• Reservation Control Desk: Reviewing all customer bookings, approving pending requests (`CONFIRMED`), rejecting invalid bookings (`REJECTED`), and handling manual cancellations.")

    add_section_heading("3.3 Database Design & E-R Diagram")
    add_body_p(
        "The relational database schema is structured around 4 core entities in Third Normal Form (3NF):"
    )
    add_bullet("USERS Entity:", "Stores user identities (`id`, `name`, `email`, `password`, `role`). Primary key: `id` (AUTO_INCREMENT). Unique key: `email`.")
    add_bullet("VEHICLES Entity:", "Stores fleet inventory (`id`, `vehicle_number`, `brand`, `model`, `type`, `price_per_day`, `status`). Primary key: `id`. Unique key: `vehicle_number`.")
    add_bullet("BOOKINGS Entity:", "Stores reservation transactions (`id`, `user_id`, `vehicle_id`, `start_date`, `end_date`, `total_amount`, `status`). Foreign keys: `user_id` references `users(id)`, `vehicle_id` references `vehicles(id)`.")
    add_bullet("PAYMENTS Entity:", "Stores payment audit records (`id`, `booking_id`, `amount`, `payment_status`, `payment_date`). Foreign key: `booking_id` references `bookings(id)`.")

    add_body_p(
        "Cardinality Relationships:\n"
        "• One User can make Zero, One, or Many Bookings (1 : M).\n"
        "• One Vehicle can be associated with Zero, One, or Many Bookings over time (1 : M).\n"
        "• One Booking can have One or More Payment attempts (1 : M)."
    )

    add_section_heading("3.4 Data Flow Diagrams (DFD)")
    add_body_p(
        "3.4.1 Level-0 Context Diagram:\n"
        "The Level-0 DFD illustrates the high-level boundary of RentRide. The two external entities—Customer and Administrator—interact "
        "with the central 'RentRide Vehicle Rental System' process. Customers provide registration data, booking requests, and mock payment tokens, "
        "receiving vehicle catalogs, booking confirmations, and receipts. Administrators supply vehicle inventory updates and approval decisions, "
        "receiving analytical revenue reports and customer reservation lists."
    )
    add_body_p(
        "3.4.2 Level-1 Detailed Data Flow Diagram:\n"
        "The system process is decomposed into 5 core subprocesses:\n"
        "1. Process 1.0 (Authentication & Authorization): Interacts with `users` data store.\n"
        "2. Process 2.0 (Fleet Catalog Management): Interacts with `vehicles` data store.\n"
        "3. Process 3.0 (Reservation & Concurrency Engine): Reads `vehicles`, validates overlaps, writes to `bookings` data store.\n"
        "4. Process 4.0 (Mock Payment Processing): Reads `bookings`, updates status, writes to `payments` data store.\n"
        "5. Process 5.0 (Admin Analytics & Fleet Control): Aggregates counts and sums from `vehicles`, `bookings`, and `payments` stores."
    )

    add_section_heading("3.5 UML Diagrams")
    add_body_p(
        "3.5.1 Use Case Diagram:\n"
        "Identifies two primary actors: Customer and Administrator.\n"
        "• Customer Use Cases: Register Account, Login, Browse Vehicles, View Vehicle Details, Book Vehicle, Make Sandbox Payment, View Booking History, Cancel Booking, Logout.\n"
        "• Administrator Use Cases: Login, View Operational Dashboard, Add Vehicle, Edit Vehicle, Toggle Vehicle Availability, Delete Vehicle, Review Bookings, Approve/Reject Bookings, Logout."
    )
    add_body_p(
        "3.5.2 Sequence Diagram (Vehicle Reservation & Payment Flow):\n"
        "1. Customer submits `POST /booking` with `vehicleId`, `startDate`, `endDate`.\n"
        "2. `BookingServlet` verifies session and date validity.\n"
        "3. `BookingServlet` calls `BookingDAO.createBooking()`.\n"
        "4. `BookingDAO` acquires pessimistic row lock on vehicle, queries for date overlaps, computes total amount, inserts `bookings` record with `PENDING` status, and commits.\n"
        "5. `BookingServlet` redirects Customer to `/payment?bookingId=X`.\n"
        "6. Customer selects payment method and submits `POST /payment`.\n"
        "7. `PaymentServlet` calls `PaymentDAO.processMockPayment()`.\n"
        "8. `PaymentDAO` locks booking, writes to `payments` table, updates booking to `CONFIRMED`, and commits transaction.\n"
        "9. `PaymentServlet` redirects Customer to `/my-bookings?payment=success`."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: CODING & IMPLEMENTATION
    # =========================================================================
    add_chapter_heading("4", "CODING & IMPLEMENTATION")

    add_section_heading("4.1 Database Scripts (schema.sql)")
    add_body_p(
        "The complete relational schema and initial seed data are defined in `schema.sql`. "
        "The tables feature cascading foreign keys and default initial administrator and customer credentials."
    )

    sql_code = (
        "-- MySQL Database Schema\n"
        "CREATE DATABASE IF NOT EXISTS rental_vehicle;\n"
        "USE rental_vehicle;\n\n"
        "CREATE TABLE IF NOT EXISTS users (\n"
        "    id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    name VARCHAR(100) NOT NULL,\n"
        "    email VARCHAR(100) NOT NULL UNIQUE,\n"
        "    password VARCHAR(255) NOT NULL,\n"
        "    role VARCHAR(20) DEFAULT 'USER'\n"
        ");\n\n"
        "CREATE TABLE IF NOT EXISTS vehicles (\n"
        "    id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    vehicle_number VARCHAR(50) NOT NULL UNIQUE,\n"
        "    brand VARCHAR(50) NOT NULL,\n"
        "    model VARCHAR(50) NOT NULL,\n"
        "    type VARCHAR(30) NOT NULL,\n"
        "    price_per_day DECIMAL(10,2) NOT NULL,\n"
        "    status VARCHAR(20) DEFAULT 'AVAILABLE'\n"
        ");\n\n"
        "CREATE TABLE IF NOT EXISTS bookings (\n"
        "    id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    user_id INT NOT NULL,\n"
        "    vehicle_id INT NOT NULL,\n"
        "    start_date DATE NOT NULL,\n"
        "    end_date DATE NOT NULL,\n"
        "    total_amount DECIMAL(10,2) NOT NULL,\n"
        "    status VARCHAR(20) DEFAULT 'PENDING',\n"
        "    CONSTRAINT fk_booking_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,\n"
        "    CONSTRAINT fk_booking_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE\n"
        ");\n\n"
        "CREATE TABLE IF NOT EXISTS payments (\n"
        "    id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    booking_id INT NOT NULL,\n"
        "    amount DECIMAL(10,2) NOT NULL,\n"
        "    payment_status VARCHAR(20) NOT NULL,\n"
        "    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    CONSTRAINT fk_payment_booking FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE\n"
        ");"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.line_spacing = 1.0
    p_code.paragraph_format.space_after = Pt(8)
    r_c = p_code.add_run(sql_code)
    r_c.font.name = 'Consolas'
    r_c.font.size = Pt(9.5)

    add_section_heading("4.2 Database Utility Layer (DBConnection.java)")
    add_body_p(
        "The `DBConnection` utility encapsulates database driver initialization and connection factory methods:"
    )

    java_dbc = (
        "package com.rental.util;\n\n"
        "import java.sql.Connection;\n"
        "import java.sql.DriverManager;\n\n"
        "public class DBConnection {\n"
        "    private static final String URL = \"jdbc:mysql://localhost:3306/rental_vehicle\";\n"
        "    private static final String USER = \"root\";\n"
        "    private static final String PASSWORD = \"chandu.4123\";\n\n"
        "    public static Connection getConnection() {\n"
        "        try {\n"
        "            Class.forName(\"com.mysql.cj.jdbc.Driver\");\n"
        "            return DriverManager.getConnection(URL, USER, PASSWORD);\n"
        "        } catch (Exception e) {\n"
        "            e.printStackTrace();\n"
        "            return null;\n"
        "        }\n"
        "    }\n"
        "}"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.line_spacing = 1.0
    p_code.paragraph_format.space_after = Pt(8)
    r_c = p_code.add_run(java_dbc)
    r_c.font.name = 'Consolas'
    r_c.font.size = Pt(9.5)

    add_section_heading("4.3 Model Entities (User, Vehicle, Booking, Payment)")
    add_body_p(
        "Plain Old Java Objects (POJOs) represent domain entities. Notably, `Vehicle.java` includes an intelligent helper method, "
        "`getImageUrl()`, which dynamically resolves static vehicle photograph assets based on vehicle models and categories:"
    )

    java_veh = (
        "public String getImageUrl() {\n"
        "    if (model != null) {\n"
        "        String m = model.toLowerCase();\n"
        "        if (m.contains(\"swift\")) return \"images/vehicles/swift.jpg\";\n"
        "        if (m.contains(\"creta\")) return \"images/vehicles/creta.jpg\";\n"
        "        if (m.contains(\"city\")) return \"images/vehicles/city.jpg\";\n"
        "        if (m.contains(\"fortuner\")) return \"images/vehicles/fortuner.jpg\";\n"
        "        if (m.contains(\"hunter\") || m.contains(\"enfield\")) return \"images/vehicles/hunter.jpg\";\n"
        "    }\n"
        "    if (type != null) {\n"
        "        String t = type.toLowerCase();\n"
        "        if (t.contains(\"hatchback\")) return \"images/vehicles/hatchback.jpg\";\n"
        "        if (t.contains(\"suv\")) return \"images/vehicles/suv.jpg\";\n"
        "        if (t.contains(\"sedan\")) return \"images/vehicles/sedan.jpg\";\n"
        "        if (t.contains(\"bike\") || t.contains(\"motorcycle\")) return \"images/vehicles/bike.jpg\";\n"
        "    }\n"
        "    return \"images/vehicles/default.jpg\";\n"
        "}"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.line_spacing = 1.0
    p_code.paragraph_format.space_after = Pt(8)
    r_c = p_code.add_run(java_veh)
    r_c.font.name = 'Consolas'
    r_c.font.size = Pt(9.5)

    add_section_heading("4.4 Concurrency & Pessimistic Locking Implementation")
    add_body_p(
        "A critical engineering feature in `BookingDAO.java` is its multi-step atomic transaction for reservation creation. "
        "The method disables auto-commit, locks the vehicle row with `FOR UPDATE`, checks for overlapping dates, computes exact days using "
        "`ChronoUnit.DAYS`, and creates the record atomically:"
    )

    java_bdao = (
        "public boolean createBooking(Booking booking) {\n"
        "    if (booking.getStartDate() == null || booking.getEndDate() == null) return false;\n"
        "    if (!booking.getEndDate().after(booking.getStartDate())) return false;\n\n"
        "    String vehicleSql = \"SELECT price_per_day, status FROM vehicles WHERE id=? FOR UPDATE\";\n"
        "    String overlapSql = \"SELECT id FROM bookings WHERE vehicle_id=? AND status IN ('PENDING','CONFIRMED') \" +\n"
        "                        \"AND start_date < ? AND end_date > ? LIMIT 1\";\n"
        "    String insertSql = \"INSERT INTO bookings(user_id, vehicle_id, start_date, end_date, total_amount, status) \" +\n"
        "                       \"VALUES(?,?,?,?,?,'PENDING')\";\n\n"
        "    try (Connection con = DBConnection.getConnection()) {\n"
        "        if (con == null) return false;\n"
        "        con.setAutoCommit(false); // Begin transaction\n\n"
        "        try {\n"
        "            // 1. Pessimistic lock and status verification\n"
        "            double pricePerDay;\n"
        "            try (PreparedStatement ps = con.prepareStatement(vehicleSql)) {\n"
        "                ps.setInt(1, booking.getVehicleId());\n"
        "                try (ResultSet rs = ps.executeQuery()) {\n"
        "                    if (!rs.next() || !\"AVAILABLE\".equalsIgnoreCase(rs.getString(\"status\"))) {\n"
        "                        con.rollback();\n"
        "                        return false;\n"
        "                    }\n"
        "                    pricePerDay = rs.getDouble(\"price_per_day\");\n"
        "                }\n"
        "            }\n\n"
        "            // 2. Overlap collision query\n"
        "            try (PreparedStatement ps = con.prepareStatement(overlapSql)) {\n"
        "                ps.setInt(1, booking.getVehicleId());\n"
        "                ps.setDate(2, booking.getEndDate());\n"
        "                ps.setDate(3, booking.getStartDate());\n"
        "                try (ResultSet rs = ps.executeQuery()) {\n"
        "                    if (rs.next()) { con.rollback(); return false; }\n"
        "                }\n"
        "            }\n\n"
        "            // 3. Precise duration calculation\n"
        "            long days = ChronoUnit.DAYS.between(booking.getStartDate().toLocalDate(), booking.getEndDate().toLocalDate());\n"
        "            if (days <= 0) days = 1;\n"
        "            double totalAmount = days * pricePerDay;\n\n"
        "            // 4. Atomic insertion\n"
        "            try (PreparedStatement ps = con.prepareStatement(insertSql, Statement.RETURN_GENERATED_KEYS)) {\n"
        "                ps.setInt(1, booking.getUserId());\n"
        "                ps.setInt(2, booking.getVehicleId());\n"
        "                ps.setDate(3, booking.getStartDate());\n"
        "                ps.setDate(4, booking.getEndDate());\n"
        "                ps.setDouble(5, totalAmount);\n"
        "                ps.executeUpdate();\n"
        "                try (ResultSet keys = ps.getGeneratedKeys()) {\n"
        "                    if (keys.next()) booking.setId(keys.getInt(1));\n"
        "                }\n"
        "            }\n"
        "            booking.setTotalAmount(totalAmount);\n"
        "            con.commit(); // Commit transaction\n"
        "            return true;\n"
        "        } catch (SQLException e) {\n"
        "            con.rollback();\n"
        "            throw e;\n"
        "        } finally {\n"
        "            con.setAutoCommit(true);\n"
        "        }\n"
        "    } catch (SQLException e) {\n"
        "        e.printStackTrace();\n"
        "        return false;\n"
        "    }\n"
        "}"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.line_spacing = 1.0
    p_code.paragraph_format.space_after = Pt(8)
    r_c = p_code.add_run(java_bdao)
    r_c.font.name = 'Consolas'
    r_c.font.size = Pt(9.0)

    add_section_heading("4.5 Security & Session Management Implementation")
    add_body_p(
        "In `LoginServlet.java`, the system prevents session fixation attacks by invalidating any existing session prior to creating "
        "a new authenticated session, setting a 30-minute inactivity timeout, and dispatching users according to their assigned role:"
    )

    java_sec = (
        "// Session fixation countermeasure\n"
        "HttpSession oldSession = request.getSession(false);\n"
        "if (oldSession != null) {\n"
        "    oldSession.invalidate();\n"
        "}\n\n"
        "HttpSession session = request.getSession(true);\n"
        "session.setAttribute(\"userId\", user.getId());\n"
        "session.setAttribute(\"userName\", user.getName());\n"
        "session.setAttribute(\"userRole\", user.getRole());\n"
        "session.setMaxInactiveInterval(30 * 60); // 30 minutes\n\n"
        "if (\"ADMIN\".equalsIgnoreCase(user.getRole())) {\n"
        "    response.sendRedirect(request.getContextPath() + \"/admin/dashboard\");\n"
        "} else {\n"
        "    response.sendRedirect(request.getContextPath() + \"/vehicles\");\n"
        "}"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.line_spacing = 1.0
    p_code.paragraph_format.space_after = Pt(8)
    r_c = p_code.add_run(java_sec)
    r_c.font.name = 'Consolas'
    r_c.font.size = Pt(9.5)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: USER INTERFACE & SCREENS
    # =========================================================================
    add_chapter_heading("5", "USER INTERFACE & SCREENS")

    add_section_heading("5.1 Customer Interface Walkthrough")
    add_body_p(
        "The customer experience is organized into an intuitive multi-step journey designed for maximum accessibility:"
    )
    add_bullet("Landing Page (`index.jsp`):", "Features an inspiring hero section ('Premium Vehicles, Uncompromised Freedom'), call-to-action buttons dynamically tailored to login state, and a features grid emphasizing Instant Booking, Verified Fleet, and Transparent Pricing.")
    add_bullet("Vehicle Catalog (`vehicles.jsp`):", "Presents available cars and motorcycles in a responsive grid. Each vehicle card renders high-definition photography, vehicle category badge (SUV, Sedan, Hatchback, Bike), registration plate, daily rate, and a direct 'View Details & Book' action.")
    add_bullet("Vehicle Details (`vehicle-details.jsp`):", "Displays an enlarged view of the vehicle, complete registration credentials, availability status badge, daily price breakdown, and immediate navigation to the booking form.")
    add_bullet("Booking Screen (`booking.jsp`):", "Provides an interactive date selection form. Embedded JavaScript enforces valid future dates and dynamically computes rental duration and estimated cost in real time.")
    add_bullet("Mock Payment Sandbox (`payment.jsp`):", "A simulated checkout console highlighting a prominent 'TEST SANDBOX' safety banner. Presents full booking summary details, radio options for simulated payment instruments (Card, UPI, Net Banking), and dedicated buttons to trigger successful authorization or simulate gateway failure.")
    add_bullet("My Reservations Console (`my-bookings.jsp`):", "A customer dashboard displaying reservation history in a data table with status badges (`PENDING`, `CONFIRMED`, `CANCELLED`). Allows customers to immediately complete pending payments or cancel active reservations.")

    add_section_heading("5.2 Administrator Dashboard & Controls")
    add_body_p(
        "Staff and administrative tools are secured under the `/admin/*` path and feature a cohesive control environment:"
    )
    add_bullet("Operational Analytics Dashboard (`admin/dashboard.jsp`):", "Displays 5 key metrics: Total Fleet Units, Active/Ready Fleet, Total Bookings, Pending Approvals, and Gross Settled Revenue. Also lists recent customer reservations with quick management shortcuts.")
    add_bullet("Fleet Inventory Management (`admin/vehicles.jsp`):", "A complete inventory control center. Staff can view all registered vehicles with thumbnail images, toggle vehicle availability (`AVAILABLE` <-> `UNAVAILABLE`) with a single click, open an edit modal to modify vehicle attributes or daily rates, and add new vehicles to the fleet.")
    add_bullet("Customer Reservations Control (`admin/bookings.jsp`):", "Administrative oversight desk listing all customer bookings, associated vehicles, rental windows, and total charges. Features staff action buttons to Approve pending bookings (`CONFIRMED`), Reject bookings (`REJECTED`), or Cancel confirmed reservations.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: TESTING & VALIDATION
    # =========================================================================
    add_chapter_heading("6", "TESTING & VALIDATION")

    add_section_heading("6.1 Testing Methodology & Objectives")
    add_body_p(
        "Quality assurance was conducted using a multi-tiered testing strategy encompassing unit testing of DAO methods, "
        "integration testing of servlets and database transactions, and end-to-end regression testing. "
        "The objective was to verify that all functional requirements, security boundaries, date validation constraints, "
        "and concurrency locks operate reliably without defect."
    )

    add_section_heading("6.2 Automated Python Test Suite (test_rental_system.py)")
    add_body_p(
        "An automated test script, `test_rental_system.py`, was engineered to simulate realistic browser interactions using Python's "
        "`urllib.request` and `http.cookiejar.CookieJar`. The script executes an end-to-end regression run across 6 sequential stages: "
        "public catalog inspection, vehicle photography verification, dynamic customer onboarding, reservation creation, "
        "sandbox payment settlement, date overlap collision rejection, and administrator portal access."
    )

    add_section_heading("6.3 Comprehensive Test Cases & Results Matrix")
    add_body_p("The table below details the formal test cases and their execution outcomes:")

    t_test = doc.add_table(rows=1, cols=4)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_t = t_test.rows[0]
    h_t.cells[0].paragraphs[0].add_run("Test ID").font.bold = True
    h_t.cells[1].paragraphs[0].add_run("Test Description & Input").font.bold = True
    h_t.cells[2].paragraphs[0].add_run("Expected Result").font.bold = True
    h_t.cells[3].paragraphs[0].add_run("Status").font.bold = True
    h_t.cells[0].width = Inches(0.8)
    h_t.cells[1].width = Inches(2.6)
    h_t.cells[2].width = Inches(2.2)
    h_t.cells[3].width = Inches(0.8)
    set_cell_shading(h_t.cells[0], "F1F5F9")
    set_cell_shading(h_t.cells[1], "F1F5F9")
    set_cell_shading(h_t.cells[2], "F1F5F9")
    set_cell_shading(h_t.cells[3], "F1F5F9")

    test_matrix = [
        ("TC-01", "GET Landing page (`/`)", "HTTP 200 OK; renders RentRide branding & navbar links", "PASS"),
        ("TC-02", "GET Static vehicle images", "HTTP 200 OK; image/jpeg served, size > 10 KB", "PASS"),
        ("TC-03", "GET Vehicles catalog (`/vehicles`)", "HTTP 200 OK; renders available vehicles & photo tags", "PASS"),
        ("TC-04", "POST Register customer with unique email", "HTTP 302 Redirect to `/login.jsp?registered=1`", "PASS"),
        ("TC-05", "POST Login customer with valid credentials", "Session established; navbar updates to user profile", "PASS"),
        ("TC-06", "GET Vehicle details (`/vehicle-details?id=2`)", "HTTP 200 OK; renders Creta specifications & CTA", "PASS"),
        ("TC-07", "POST Create booking for Vehicle 2", "Booking created with `PENDING` status; redirect to `/payment`", "PASS"),
        ("TC-08", "GET Payment sandbox (`/payment?bookingId=X`)", "HTTP 200 OK; renders sandbox banner & payment options", "PASS"),
        ("TC-09", "POST Process mock payment as SUCCESS", "Transaction commits; booking status updated to `CONFIRMED`", "PASS"),
        ("TC-10", "POST Booking with overlapping date window", "Request rejected; error message displayed to user", "PASS"),
        ("TC-11", "POST Admin login (`admin@rental.com`)", "Authenticated; redirected to `/admin/dashboard`", "PASS"),
        ("TC-12", "GET Admin dashboard (`/admin/dashboard`)", "HTTP 200 OK; renders 5 KPI metric cards & gross revenue", "PASS"),
        ("TC-13", "GET Admin fleet management (`/admin/vehicles`)", "HTTP 200 OK; renders inventory table with edit modals", "PASS"),
        ("TC-14", "GET Admin reservation control (`/admin/bookings`)", "HTTP 200 OK; renders bookings table with staff actions", "PASS")
    ]

    for tid, tdesc, texp, tstat in test_matrix:
        row = t_test.add_row()
        row.cells[0].width = Inches(0.8)
        row.cells[1].width = Inches(2.6)
        row.cells[2].width = Inches(2.2)
        row.cells[3].width = Inches(0.8)
        row.cells[0].paragraphs[0].add_run(tid).font.bold = True
        row.cells[1].paragraphs[0].add_run(tdesc)
        row.cells[2].paragraphs[0].add_run(texp)
        r_s = row.cells[3].paragraphs[0].add_run(tstat)
        r_s.font.bold = True
        r_s.font.color.rgb = RGBColor(22, 163, 74)
        for c in row.cells:
            set_cell_border(c, bottom=dict(sz=2, val='single', color='E2E8F0'))

    add_section_heading("6.4 Concurrency & Edge-Case Validation")
    add_body_p(
        "A dedicated automated test (TC-10) was executed to validate the system's concurrency defense. "
        "When an attempt was made to reserve Vehicle 2 during a date window overlapping with an already confirmed booking, "
        "the database overlap query immediately caught the conflict. The transaction was cleanly rolled back, and the client was "
        "presented with an informative error message ('Vehicle is unavailable or has an overlapping booking for the selected dates'), "
        "demonstrating complete scheduling safety."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: CONCLUSION & FUTURE ENHANCEMENTS
    # =========================================================================
    add_chapter_heading("7", "CONCLUSION & FUTURE ENHANCEMENTS")

    add_section_heading("7.1 Conclusion")
    add_body_p(
        "The “RentRide” (Vehicle Rental System) project successfully demonstrates the design, implementation, and deployment "
        "of an enterprise-grade web application built upon Java EE principles and relational database design. "
        "By adhering strictly to the Model-View-Controller (MVC) architecture, the system achieves a clean separation between presentation "
        "logic, request orchestration, and data persistence."
    )
    add_body_p(
        "The project directly addresses the operational bottlenecks of traditional vehicle rentals through automated self-service scheduling, "
        "transparent client-side and server-side pricing calculations, cryptographic password hashing via jBCrypt, session-fixation protection, "
        "and a safe mock payment sandbox. Crucially, the implementation of database-level pessimistic locking (`SELECT ... FOR UPDATE`) "
        "and date overlap algorithms guarantees zero double-booking occurrences. Automated regression testing confirmed 100% compliance "
        "across all functional test scenarios, proving that RentRide is robust, secure, and ready for practical deployment."
    )

    add_section_heading("7.2 Future Enhancements")
    add_body_p(
        "While the current release provides a comprehensive core rental platform, prospective enhancements for future versions include:"
    )
    add_bullet("1. Commercial Payment Gateway Integration:", "Integrating production banking APIs (e.g., Razorpay, Stripe, PayPal) with secure webhook listeners for automated digital receipts and refunds.")
    add_bullet("2. IoT & GPS Fleet Telemetry:", "Interfacing with on-vehicle OBD-II GPS hardware to monitor real-time vehicle geographical coordinates, fuel levels, and odometer readings.")
    add_bullet("3. Automated Digital Agreement Signing:", "Enabling customers to upload government identification (Driving License, National ID) with automated OCR verification and digital signature capture.")
    add_bullet("4. Mobile Application Deployment:", "Developing native Android and iOS mobile applications utilizing cross-platform frameworks (e.g., Flutter or React Native) connected via RESTful JSON web services.")
    add_bullet("5. Customer Review & Rating Engine:", "Allowing verified customers to submit feedback, ratings, and vehicle performance reviews following completed journeys.")

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    p_ref = doc.add_paragraph()
    p_ref.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ref = p_ref.add_run("REFERENCES")
    r_ref.font.bold = True
    r_ref.font.size = Pt(15)
    r_ref.underline = True
    p_ref.paragraph_format.space_after = Pt(16)

    references = [
        "1. Herbert Schildt, “Java: The Complete Reference”, 12th Edition, McGraw-Hill Education, 2021.",
        "2. Bryan Basham, Kathy Sierra, and Bert Bates, “Head First Servlets and JSP”, 2nd Edition, O'Reilly Media, 2008.",
        "3. Marty Hall and Larry Brown, “Core Servlets and JavaServer Pages”, Volume 1: Core Technologies, 2nd Edition, Prentice Hall, 2003.",
        "4. Paul DuBois, “MySQL: Developer's Library”, 5th Edition, Addison-Wesley Professional, 2013.",
        "5. Damien Miller, “jBCrypt: Strong Password Hashing for Java”, Mindrot Security Software, https://www.mindrot.org/projects/jBCrypt/.",
        "6. Oracle Corporation, “Java Servlet 4.0 Specification (JSR 369)”, Eclipse Foundation, 2017.",
        "7. Apache Software Foundation, “Apache Tomcat 9.0 Documentation”, https://tomcat.apache.org/tomcat-9.0-doc/.",
        "8. Mozilla Developer Network (MDN), “MDN Web Docs: HTML5, CSS3, and JavaScript Guides”, https://developer.mozilla.org/.",
        "9. World Wide Web Consortium (W3C), “W3C Recommendations for Cascading Style Sheets and Web Accessibility”, https://www.w3.org/."
    ]

    for r in references:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.line_spacing = 1.3
        p_r.paragraph_format.space_after = Pt(8)
        p_r.add_run(r)

    # Save Document
    output_filename = "VEHICLE_RENTAL_SYSTEM_PROJECT_REPORT.docx"
    doc.save(output_filename)
    print(f"Academic Report generated successfully: {output_filename}")

if __name__ == "__main__":
    build_report()
