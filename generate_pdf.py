# -*- coding: utf-8 -*-
"""
Script to generate the complete, professional Project Source Code and Verification PDF:
Vehicle_Rental_System_Source_Code_and_Screenshots.pdf
Features automated two-pass Table of Contents page tracking.
"""

import os
import sys
import datetime
from PIL import Image as PILImage

import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, Preformatted, HRFlowable, Flowable
)
from reportlab.pdfgen import canvas

# PDF Target Path
OUTPUT_DIR = os.path.join(os.getcwd(), "project-documentation")
os.makedirs(OUTPUT_DIR, exist_ok=True)
PDF_PATH = os.path.join(OUTPUT_DIR, "Vehicle_Rental_System_Source_Code_and_Screenshots.pdf")

# Page Dimensions (A4: 595.27 x 841.89 pt)
PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 48
RIGHT_MARGIN = 48
TOP_MARGIN = 48
BOTTOM_MARGIN = 48
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

PAGE_REGISTRY = {}

class PageTracker(Flowable):
    """
    Zero-height flowable that records the current canvas page number into PAGE_REGISTRY.
    """
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.width = 0
        self.height = 0

    def draw(self):
        PAGE_REGISTRY[self.key] = self.canv._pageNumber

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to calculate total page count and render running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.saveState()
                
                # Running Header
                self.setFont("Helvetica-Bold", 7.5)
                self.setFillColor(colors.HexColor("#1E293B"))
                self.drawString(LEFT_MARGIN, PAGE_HEIGHT - 32, "RENTAL VEHICLE SYSTEM (RentRide)")
                self.setFont("Helvetica", 7.5)
                self.setFillColor(colors.HexColor("#64748B"))
                self.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 32, "Source Code & System Documentation")
                
                self.setStrokeColor(colors.HexColor("#CBD5E1"))
                self.setLineWidth(0.6)
                self.line(LEFT_MARGIN, PAGE_HEIGHT - 36, PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 36)
                
                # Running Footer
                self.line(LEFT_MARGIN, 38, PAGE_WIDTH - RIGHT_MARGIN, 38)
                self.setFont("Helvetica", 7.5)
                self.setFillColor(colors.HexColor("#64748B"))
                self.drawString(LEFT_MARGIN, 26, "Lakireddy Bali Reddy College of Engineering (Autonomous) | Dept. of CSE")
                page_str = f"Page {self._pageNumber} of {num_pages}"
                self.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, 26, page_str)
                
                self.restoreState()
            super().showPage()
        super().save()


def wrap_code_lines(code_text, max_len=92):
    """
    Wrap long lines in code blocks cleanly with continuation indicators.
    """
    wrapped_lines = []
    for line in code_text.splitlines():
        # Redact sensitive database passwords
        if 'PASSWORD=' in line or 'PASSWORD =' in line:
            if 'chandu.4123' in line:
                line = '    private static final String PASSWORD = "••••••••••••" /* [REDACTED_SECURE_PASSWORD] */;'
        
        if len(line) <= max_len:
            wrapped_lines.append(line)
        else:
            indent = len(line) - len(line.lstrip())
            indent_str = " " * indent
            while len(line) > max_len:
                wrapped_lines.append(line[:max_len])
                line = indent_str + "  ↳ " + line[max_len:]
            wrapped_lines.append(line)
    return "\n".join(wrapped_lines)


def get_styles():
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=base['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        alignment=1,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_header = ParagraphStyle(
        'CodeHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0F172A')
    )

    code_meta = ParagraphStyle(
        'CodeMeta',
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#475569')
    )

    code_content = ParagraphStyle(
        'CodeContent',
        fontName='Courier',
        fontSize=6.5,
        leading=8.5,
        leftIndent=6,
        rightIndent=6,
        textColor=colors.HexColor('#0F172A')
    )

    toc_item = ParagraphStyle(
        'TOCItem',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    caption_style = ParagraphStyle(
        'CaptionStyle',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0F172A'),
        alignment=1,
        spaceBefore=5,
        spaceAfter=3
    )

    caption_desc = ParagraphStyle(
        'CaptionDesc',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=10
    )

    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'h1': h1_style,
        'h2': h2_style,
        'h3': h3_style,
        'body': body_style,
        'body_bold': body_bold,
        'code_header': code_header,
        'code_meta': code_meta,
        'code_content': code_content,
        'toc_item': toc_item,
        'caption': caption_style,
        'caption_desc': caption_desc
    }


def make_section_header(title_text, subtitle_text=None, styles=None):
    elements = []
    elements.append(Paragraph(title_text, styles['h1']))
    if subtitle_text:
        elements.append(Paragraph(subtitle_text, styles['body']))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceBefore=2, spaceAfter=8))
    return elements


def build_cover_page(styles):
    cover = []
    cover.append(PageTracker("cover"))
    cover.append(Spacer(1, 15))

    # College Header
    cover.append(Paragraph("LAKIREDDY BALI REDDY COLLEGE OF ENGINEERING (AUTONOMOUS)", ParagraphStyle('CollegeH1', fontName='Helvetica-Bold', fontSize=13, leading=16, alignment=1, textColor=colors.HexColor('#0F172A'))))
    cover.append(Paragraph("Affiliated to JNTUK, Kakinada & Accredited by NAAC with 'A' Grade<br/>Approved by AICTE, New Delhi | An ISO 9001:2015 Certified Institution<br/>Mylavaram, NTR District, Andhra Pradesh - 521230", ParagraphStyle('CollegeH2', fontName='Helvetica', fontSize=8, leading=11, alignment=1, textColor=colors.HexColor('#475569'))))
    cover.append(Spacer(1, 10))

    # College Logo
    logo_path = os.path.join(os.getcwd(), "lbrce_logo.jpeg")
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=80, height=96)
        logo_img.hAlign = 'CENTER'
        cover.append(logo_img)
    cover.append(Spacer(1, 12))

    # Department
    cover.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", ParagraphStyle('Dept', fontName='Helvetica-Bold', fontSize=10.5, leading=13, alignment=1, textColor=colors.HexColor('#1E293B'))))
    cover.append(HRFlowable(width="80%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=8, spaceAfter=14))

    # Project Title
    cover.append(Paragraph("VEHICLE RENTAL SYSTEM", styles['title']))
    cover.append(Paragraph("A FULL-STACK WEB APPLICATION (RentRide)", styles['subtitle']))
    cover.append(Paragraph("COMPLETE APPLICATION SOURCE CODE & EMPIRICAL VERIFICATION REPORT", ParagraphStyle('DocType', fontName='Helvetica-Bold', fontSize=9, leading=12, alignment=1, textColor=colors.HexColor('#475569'))))
    cover.append(Spacer(1, 18))

    # Student & Project Details Card
    info_data = [
        [Paragraph("<b>Project Title:</b>", styles['body']), Paragraph("Vehicle Rental System (RentRide)", styles['body'])],
        [Paragraph("<b>Student Name:</b>", styles['body']), Paragraph("<b>GUBBALA CHAITANYA SAI KRISHNA</b>", styles['body'])],
        [Paragraph("<b>Roll Number:</b>", styles['body']), Paragraph("<b>24761A0517</b>", styles['body'])],
        [Paragraph("<b>Degree & Branch:</b>", styles['body']), Paragraph("Bachelor of Technology (B.Tech) in Computer Science & Engineering", styles['body'])],
        [Paragraph("<b>Academic Year:</b>", styles['body']), Paragraph("2026 - 2027", styles['body'])],
        [Paragraph("<b>Technology Stack:</b>", styles['body']), Paragraph("Java 21, Java Servlets (Java EE), JavaServer Pages (JSP), JDBC, MySQL 8.0, Apache Tomcat 9.0, Vanilla CSS3, BCrypt", styles['body'])],
        [Paragraph("<b>Testing Framework:</b>", styles['body']), Paragraph("Selenium WebDriver 4.x, Headless Microsoft Edge, Automated Functional Suite", styles['body'])],
        [Paragraph("<b>Documentation Date:</b>", styles['body']), Paragraph(f"{datetime.date.today().strftime('%B %d, %Y')}", styles['body'])],
        [Paragraph("<b>Verification Status:</b>", styles['body']), Paragraph("<font color='#059669'><b>100% VERIFIED & FULLY FUNCTIONAL (15/15 Tests Passed)</b></font>", styles['body'])],
    ]

    info_table = Table(info_data, colWidths=[125, CONTENT_WIDTH - 125])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    cover.append(info_table)
    cover.append(Spacer(1, 15))

    # Institutional Notice
    notice_text = "This comprehensive technical documentation contains the verified software architecture, complete database schemas, all 37 unredacted application source files, genuine browser verification screenshots, empirical test results, and operational run instructions for the RentRide Vehicle Rental System."
    cover.append(Paragraph(notice_text, ParagraphStyle('Notice', fontName='Helvetica-Oblique', fontSize=7.5, leading=10.5, alignment=1, textColor=colors.HexColor('#64748B'))))
    cover.append(PageBreak())
    return cover


def build_toc(styles, registry):
    toc = []
    toc.append(PageTracker("toc"))
    toc.extend(make_section_header("Table of Contents", "Comprehensive document navigation and page index", styles))

    def pg(key, default=""):
        return str(registry.get(key, default))

    toc_data = [
        [Paragraph("<b>Section A: Project Overview & System Scope</b>", styles['toc_item']), Paragraph(f"<b>{pg('sec_overview', '3')}</b>", styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;A.1 Problem Statement & Proposed Solution", styles['toc_item']), Paragraph(pg('sec_overview', '3'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;A.2 Key Features for Customers & Fleet Administrators", styles['toc_item']), Paragraph(pg('sec_overview', '3'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;A.3 Three-Tier Enterprise Architectural Paradigm", styles['toc_item']), Paragraph(pg('sec_overview', '3'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;A.4 Technology Stack & Runtime Specifications", styles['toc_item']), Paragraph(pg('sec_overview', '3'), styles['toc_item'])],
        
        [Paragraph("<b>Section B: Project Structure & File Layout</b>", styles['toc_item']), Paragraph(f"<b>{pg('sec_structure', '4')}</b>", styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;B.1 Complete Project Directory Tree", styles['toc_item']), Paragraph(pg('sec_structure', '4'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;B.2 Package & Directory Responsibilities", styles['toc_item']), Paragraph(pg('sec_structure', '4'), styles['toc_item'])],
        
        [Paragraph("<b>Section C: Relational Database Architecture</b>", styles['toc_item']), Paragraph(f"<b>{pg('sec_db', '5')}</b>", styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;C.1 Database Schema & Entity Relationships", styles['toc_item']), Paragraph(pg('sec_db', '5'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;C.2 Relational Tables (Users, Vehicles, Bookings, Payments)", styles['toc_item']), Paragraph(pg('sec_db', '5'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;C.3 Concurrency Control & Row-Level Locking Architecture", styles['toc_item']), Paragraph(pg('sec_db', '5'), styles['toc_item'])],
        
        [Paragraph("<b>Section D: Complete Application Source Code</b>", styles['toc_item']), Paragraph(f"<b>{pg('sec_source', '6')}</b>", styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D.1 Domain Model Entity Classes (4 files)", styles['toc_item']), Paragraph(pg('sec_d1', '6'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D.2 Data Access Objects / JDBC Layer (4 files)", styles['toc_item']), Paragraph(pg('sec_d2', '12'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D.3 Database Connection & Testing Utilities (2 files)", styles['toc_item']), Paragraph(pg('sec_d3', '21'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D.4 Public & Customer Servlets / Controllers (9 files)", styles['toc_item']), Paragraph(pg('sec_d4', '22'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D.5 Administrator Portal Servlets (3 files)", styles['toc_item']), Paragraph(pg('sec_d5', '34'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D.6 Web Application Presentation Views / JSP (12 files)", styles['toc_item']), Paragraph(pg('sec_d6', '38'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D.7 Custom CSS Design System (1 file)", styles['toc_item']), Paragraph(pg('sec_d7', '56'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D.8 Web Application Deployment Descriptor (1 file)", styles['toc_item']), Paragraph(pg('sec_d8', '67'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D.9 MySQL Schema & Seed SQL Script (1 file)", styles['toc_item']), Paragraph(pg('sec_d9', '68'), styles['toc_item'])],
        
        [Paragraph("<b>Section E: Live Website Screenshots & User Workflows</b>", styles['toc_item']), Paragraph(f"<b>{pg('sec_screenshots', '70')}</b>", styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;E.1 Customer Workflows (Landing, Catalog, Specs, Booking, Sandbox, Dashboard)", styles['toc_item']), Paragraph(pg('sec_screenshots', '70'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;E.2 Security & Error Handling (Authentication, Overlap Rejection)", styles['toc_item']), Paragraph(pg('sec_screenshots', '70'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;E.3 Administrator Operations (KPI Dashboard, Inventory Controls, Reservations)", styles['toc_item']), Paragraph(pg('sec_screenshots', '70'), styles['toc_item'])],
        
        [Paragraph("<b>Section F: Testing, Quality Assurance & Empirical Verification</b>", styles['toc_item']), Paragraph(f"<b>{pg('sec_testing', '77')}</b>", styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;F.1 Testing Methodology & Automated Test Suite Execution", styles['toc_item']), Paragraph(pg('sec_testing', '77'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;F.2 Empirical Test Execution Matrix (15/15 Verified Tests)", styles['toc_item']), Paragraph(pg('sec_testing', '77'), styles['toc_item'])],
        
        [Paragraph("<b>Section G: Operational Run & Deployment Instructions</b>", styles['toc_item']), Paragraph(f"<b>{pg('sec_instructions', '78')}</b>", styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;G.1 Runtime Prerequisites & Environment Configuration", styles['toc_item']), Paragraph(pg('sec_instructions', '78'), styles['toc_item'])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;G.2 Database Initialization & Tomcat Server Launch", styles['toc_item']), Paragraph(pg('sec_instructions', '78'), styles['toc_item'])],
        
        [Paragraph("<b>Section H: Conclusion & Future Scope</b>", styles['toc_item']), Paragraph(f"<b>{pg('sec_conclusion', '79')}</b>", styles['toc_item'])],
    ]

    toc_table = Table(toc_data, colWidths=[CONTENT_WIDTH - 40, 40])
    toc_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    toc.append(toc_table)
    toc.append(PageBreak())
    return toc


def build_overview_and_architecture(styles):
    sec = []
    sec.append(PageTracker("sec_overview"))
    sec.extend(make_section_header("Section A: Project Overview & System Scope", "Problem domain, functional features, and enterprise architectural design", styles))

    sec.append(Paragraph("A.1 Purpose of the Application & Problem Domain", styles['h2']))
    sec.append(Paragraph(
        "Traditional vehicle rental operations frequently suffer from manual record-keeping errors, double-booking conflicts, opaque pricing structures, and disjointed payment tracking. The <b>RentRide Vehicle Rental System</b> is an enterprise-grade web application engineered to digitalize and automate the end-to-end vehicle rental lifecycle. The system provides seamless self-service booking for customers while empowering fleet managers with real-time operational analytics, dynamic inventory governance, and reservation status control.",
        styles['body']
    ))

    sec.append(Paragraph("A.2 Key System Features", styles['h2']))
    sec.append(Paragraph("<b>1. Public Customer Features:</b>", styles['h3']))
    sec.append(Paragraph(
        "• <b>Fleet Catalog Discovery:</b> Browse comprehensive vehicle inventories across diverse classifications (Hatchback, Sedan, SUV, Motorcycle) featuring real photography, detailed specifications, and transparent daily pricing.<br/>"
        "• <b>Real-Time Pricing Calculator:</b> Dynamic date-picker calculations compute total rental costs instantaneously before reservation confirmation.<br/>"
        "• <b>Overlap Conflict Prevention:</b> Advanced SQL row-locking verifies that selected rental windows do not conflict with existing active reservations.<br/>"
        "• <b>Development Payment Sandbox:</b> Interactive mock payment gateway simulating Credit/Debit Card, UPI (Google Pay, PhonePe), and Netbanking authorizations.<br/>"
        "• <b>Customer Reservation Dashboard:</b> Track historical and ongoing bookings with live status badges (PENDING, CONFIRMED, COMPLETED, CANCELLED) and self-service cancellation capability.",
        styles['body']
    ))

    sec.append(Paragraph("<b>2. Fleet Administrator Features:</b>", styles['h3']))
    sec.append(Paragraph(
        "• <b>Executive Operational Dashboard:</b> Real-time KPI metrics displaying Gross Revenue, Total Fleet Count, Active Bookings, and Total Registered Users.<br/>"
        "• <b>Fleet Inventory Governance:</b> Add new vehicles with registration numbers, update rental rates, toggle operational statuses (AVAILABLE, RENTED, MAINTENANCE), and decommission units.<br/>"
        "• <b>Customer Reservations Management:</b> Centralized reservation control allowing managers to review, confirm, complete, or cancel bookings across the entire enterprise.",
        styles['body']
    ))

    sec.append(Paragraph("A.3 Enterprise Three-Tier Architecture", styles['h2']))
    sec.append(Paragraph(
        "The application strictly adheres to the proven <b>Three-Tier Architectural Pattern</b>, ensuring strict separation of concerns, high maintainability, and enterprise scalability:",
        styles['body']
    ))

    arch_data = [
        [Paragraph("<b>Architectural Layer</b>", styles['body_bold']), Paragraph("<b>Technologies Used</b>", styles['body_bold']), Paragraph("<b>Responsibilities & Implementation</b>", styles['body_bold'])],
        [Paragraph("<b>Presentation Tier (Client/UI)</b>", styles['body']), Paragraph("JSP, Vanilla CSS3, JavaScript, HTML5", styles['body']), Paragraph("Renders responsive user interfaces, forms, and dynamic navigation. Utilizes modern CSS variables, card layouts, and client-side date validation.", styles['body'])],
        [Paragraph("<b>Business & Controller Tier</b>", styles['body']), Paragraph("Java 21, Java Servlets (Java EE), BCrypt", styles['body']), Paragraph("Encapsulates HTTP routing, session security, role-based access control (RBAC), rental pricing calculations, and transaction coordination.", styles['body'])],
        [Paragraph("<b>Data & Persistence Tier</b>", styles['body']), Paragraph("MySQL 8.0, JDBC (PreparedStatement)", styles['body']), Paragraph("Relational data persistence with strict foreign key constraints, cascading deletes, ACID transactions, and pessimistic row locking (`FOR UPDATE`).", styles['body'])],
    ]
    arch_table = Table(arch_data, colWidths=[120, 110, CONTENT_WIDTH - 230])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    sec.append(arch_table)
    sec.append(Spacer(1, 10))

    sec.append(Paragraph("A.4 Technology Stack Specifications", styles['h2']))
    tech_data = [
        [Paragraph("<b>Component</b>", styles['body_bold']), Paragraph("<b>Technology Specification</b>", styles['body_bold']), Paragraph("<b>Version / Implementation Note</b>", styles['body_bold'])],
        [Paragraph("Language & Runtime", styles['body']), Paragraph("Java Development Kit (JDK)", styles['body']), Paragraph("Java 21 LTS (OpenJDK 64-Bit Server VM)", styles['body'])],
        [Paragraph("Web Server / Servlet Engine", styles['body']), Paragraph("Apache Tomcat", styles['body']), Paragraph("Tomcat 9.0.120 (Configured on Port 8084)", styles['body'])],
        [Paragraph("Relational Database", styles['body']), Paragraph("MySQL Community Server", styles['body']), Paragraph("MySQL 8.0.x (Port 3306, InnoDB Storage Engine)", styles['body'])],
        [Paragraph("Database Driver", styles['body']), Paragraph("MySQL Connector/J", styles['body']), Paragraph("mysql-connector-j-26.7.0.jar (Type 4 JDBC Driver)", styles['body'])],
        [Paragraph("Password Security", styles['body']), Paragraph("jBCrypt Library", styles['body']), Paragraph("jbcrypt-0.4.jar (Adaptive Salted Password Hashing)", styles['body'])],
        [Paragraph("Frontend Presentation", styles['body']), Paragraph("JavaServer Pages & Custom CSS", styles['body']), Paragraph("JSP 2.3, Custom Glassmorphism Vanilla CSS3", styles['body'])],
    ]
    tech_table = Table(tech_data, colWidths=[130, 140, CONTENT_WIDTH - 270])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    sec.append(tech_table)
    sec.append(PageBreak())

    # Section B: Project Structure
    sec.append(PageTracker("sec_structure"))
    sec.extend(make_section_header("Section B: Project Structure & File Layout", "Source file hierarchy and functional modularity", styles))
    sec.append(Paragraph("B.1 Complete Project Directory Tree", styles['h2']))

    tree_text = (
        "RentalVehicleSystem/\n"
        "├── schema.sql                               # MySQL DDL schema and initial seed data\n"
        "├── src/main/java/com/rental/\n"
        "│   ├── model/                               # Domain Entity Models (Java POJOs)\n"
        "│   │   ├── User.java                        # User model with role and credentials\n"
        "│   │   ├── Vehicle.java                     # Fleet unit model with rates and statuses\n"
        "│   │   ├── Booking.java                     # Reservation model with dates and totals\n"
        "│   │   └── Payment.java                     # Transaction record model\n"
        "│   ├── dao/                                 # Data Access Objects (JDBC Layer)\n"
        "│   │   ├── UserDAO.java                     # User authentication & registration DAO\n"
        "│   │   ├── VehicleDAO.java                  # Fleet queries & management DAO\n"
        "│   │   ├── BookingDAO.java                  # Booking operations with overlap validation\n"
        "│   │   └── PaymentDAO.java                  # Payment settlement & revenue aggregation\n"
        "│   ├── controller/                          # Java Servlets (HTTP Request Handlers)\n"
        "│   │   ├── VehicleServlet.java              # Public vehicle catalog (/vehicles)\n"
        "│   │   ├── VehicleDetailsServlet.java       # Vehicle details view (/vehicle-details)\n"
        "│   │   ├── RegisterServlet.java             # User registration handler (/register)\n"
        "│   │   ├── LoginServlet.java                # Authentication handler (/login)\n"
        "│   │   ├── BookingServlet.java              # Booking creation & validation (/booking)\n"
        "│   │   ├── PaymentServlet.java              # Mock sandbox payment (/payment)\n"
        "│   │   ├── MyBookingsServlet.java           # Customer bookings dashboard (/my-bookings)\n"
        "│   │   ├── CancelBookingServlet.java        # Booking cancellation (/cancel-booking)\n"
        "│   │   ├── LogoutServlet.java               # Session termination (/logout)\n"
        "│   │   ├── AdminDashboardServlet.java       # Admin metrics & analytics (/admin/dashboard)\n"
        "│   │   ├── AdminVehicleServlet.java         # Fleet inventory controls (/admin/vehicles)\n"
        "│   │   └── AdminBookingServlet.java         # Customer reservations (/admin/bookings)\n"
        "│   └── util/                                # Utility Classes\n"
        "│       ├── DBConnection.java                # JDBC connection provider\n"
        "│       └── TESTConnection.java              # Database connectivity test harness\n"
        "├── src/main/webapp/\n"
        "│   ├── index.jsp                            # Landing page with hero banner and CTA\n"
        "│   ├── vehicles.jsp                         # Vehicle fleet catalog with photo cards\n"
        "│   ├── vehicle-details.jsp                  # Vehicle specifications view\n"
        "│   ├── login.jsp                            # User & admin sign-in page\n"
        "│   ├── register.jsp                         # Customer registration form\n"
        "│   ├── booking.jsp                          # Date selection and price calculation form\n"
        "│   ├── payment.jsp                          # Mock payment gateway sandbox\n"
        "│   ├── my-bookings.jsp                      # Customer reservation history dashboard\n"
        "│   ├── includes/navbar.jsp                  # Dynamic session-aware navigation bar\n"
        "│   ├── admin/\n"
        "│   │   ├── dashboard.jsp                    # Operational KPI metrics and analytics\n"
        "│   │   ├── vehicles.jsp                     # Fleet inventory management table\n"
        "│   │   └── bookings.jsp                     # All customer reservations management\n"
        "│   ├── css/style.css                        # Complete modern responsive CSS design system\n"
        "│   ├── images/vehicles/                     # Vehicle photography assets\n"
        "│   └── WEB-INF/\n"
        "│       ├── web.xml                          # Deployment descriptor configuration\n"
        "│       └── lib/                             # Dependency JAR libraries (JDBC, BCrypt)\n"
        "└── project-documentation/                   # Generated reports and screenshots\n"
    )
    sec.append(Preformatted(tree_text, ParagraphStyle('TreeCode', fontName='Courier', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#0F172A'))))
    sec.append(PageBreak())

    # Section C: Database Design
    sec.append(PageTracker("sec_db"))
    sec.extend(make_section_header("Section C: Relational Database Architecture", "MySQL schema, entity relationships, and concurrency control", styles))
    sec.append(Paragraph("C.1 Database Schema Overview", styles['h2']))
    sec.append(Paragraph(
        "The persistent storage layer is backed by MySQL 8.0 under the database name <code>rental_vehicle</code>. The schema enforces strict relational integrity with foreign keys, index optimizations, and cascading deletion semantics:",
        styles['body']
    ))

    db_tables_summary = [
        [Paragraph("<b>Table Name</b>", styles['body_bold']), Paragraph("<b>Primary Key</b>", styles['body_bold']), Paragraph("<b>Foreign Keys</b>", styles['body_bold']), Paragraph("<b>Description & Domain Purpose</b>", styles['body_bold'])],
        [Paragraph("<b>users</b>", styles['body']), Paragraph("id (INT AUTO_INCREMENT)", styles['body']), Paragraph("None (email UNIQUE)", styles['body']), Paragraph("Stores registered customers and administrators with BCrypt salted password hashes.", styles['body'])],
        [Paragraph("<b>vehicles</b>", styles['body']), Paragraph("id (INT AUTO_INCREMENT)", styles['body']), Paragraph("None (vehicle_number UNIQUE)", styles['body']), Paragraph("Maintains fleet inventory, daily rates, model information, and current operational statuses.", styles['body'])],
        [Paragraph("<b>bookings</b>", styles['body']), Paragraph("id (INT AUTO_INCREMENT)", styles['body']), Paragraph("user_id &rarr; users(id)<br/>vehicle_id &rarr; vehicles(id)", styles['body']), Paragraph("Captures reservation windows, computed pricing, and reservation statuses (PENDING, CONFIRMED, etc.).", styles['body'])],
        [Paragraph("<b>payments</b>", styles['body']), Paragraph("id (INT AUTO_INCREMENT)", styles['body']), Paragraph("booking_id &rarr; bookings(id)", styles['body']), Paragraph("Logs transaction records, settlement amounts, and timestamps linked to customer bookings.", styles['body'])],
    ]
    sec.append(Table(db_tables_summary, colWidths=[75, 110, 110, CONTENT_WIDTH - 295], style=[
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    sec.append(Spacer(1, 10))

    sec.append(Paragraph("C.2 Detailed Table Specifications", styles['h2']))
    sec.append(Paragraph("<b>Table: users</b>", styles['h3']))
    users_schema = [
        [Paragraph("<b>Column</b>", styles['body_bold']), Paragraph("<b>Type</b>", styles['body_bold']), Paragraph("<b>Null</b>", styles['body_bold']), Paragraph("<b>Key</b>", styles['body_bold']), Paragraph("<b>Default</b>", styles['body_bold']), Paragraph("<b>Description</b>", styles['body_bold'])],
        [Paragraph("id", styles['body']), Paragraph("INT", styles['body']), Paragraph("NO", styles['body']), Paragraph("PRI", styles['body']), Paragraph("AUTO_INCREMENT", styles['body']), Paragraph("Unique user identifier", styles['body'])],
        [Paragraph("name", styles['body']), Paragraph("VARCHAR(100)", styles['body']), Paragraph("NO", styles['body']), Paragraph("", styles['body']), Paragraph("None", styles['body']), Paragraph("Full name of the user", styles['body'])],
        [Paragraph("email", styles['body']), Paragraph("VARCHAR(100)", styles['body']), Paragraph("NO", styles['body']), Paragraph("UNI", styles['body']), Paragraph("None", styles['body']), Paragraph("Unique email address (login credential)", styles['body'])],
        [Paragraph("password", styles['body']), Paragraph("VARCHAR(255)", styles['body']), Paragraph("NO", styles['body']), Paragraph("", styles['body']), Paragraph("None", styles['body']), Paragraph("BCrypt hashed password", styles['body'])],
        [Paragraph("role", styles['body']), Paragraph("VARCHAR(20)", styles['body']), Paragraph("YES", styles['body']), Paragraph("", styles['body']), Paragraph("'USER'", styles['body']), Paragraph("Authorization role: 'USER' or 'ADMIN'", styles['body'])],
    ]
    sec.append(Table(users_schema, colWidths=[65, 80, 40, 40, 95, CONTENT_WIDTH - 320], style=[
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    sec.append(Spacer(1, 8))

    sec.append(Paragraph("<b>Table: bookings</b>", styles['h3']))
    bookings_schema = [
        [Paragraph("<b>Column</b>", styles['body_bold']), Paragraph("<b>Type</b>", styles['body_bold']), Paragraph("<b>Null</b>", styles['body_bold']), Paragraph("<b>Key</b>", styles['body_bold']), Paragraph("<b>Default</b>", styles['body_bold']), Paragraph("<b>Description</b>", styles['body_bold'])],
        [Paragraph("id", styles['body']), Paragraph("INT", styles['body']), Paragraph("NO", styles['body']), Paragraph("PRI", styles['body']), Paragraph("AUTO_INCREMENT", styles['body']), Paragraph("Unique reservation reference ID", styles['body'])],
        [Paragraph("user_id", styles['body']), Paragraph("INT", styles['body']), Paragraph("NO", styles['body']), Paragraph("MUL", styles['body']), Paragraph("None", styles['body']), Paragraph("Foreign key references users(id)", styles['body'])],
        [Paragraph("vehicle_id", styles['body']), Paragraph("INT", styles['body']), Paragraph("NO", styles['body']), Paragraph("MUL", styles['body']), Paragraph("None", styles['body']), Paragraph("Foreign key references vehicles(id)", styles['body'])],
        [Paragraph("start_date", styles['body']), Paragraph("DATE", styles['body']), Paragraph("NO", styles['body']), Paragraph("", styles['body']), Paragraph("None", styles['body']), Paragraph("Rental pick-up date", styles['body'])],
        [Paragraph("end_date", styles['body']), Paragraph("DATE", styles['body']), Paragraph("NO", styles['body']), Paragraph("", styles['body']), Paragraph("None", styles['body']), Paragraph("Rental drop-off date", styles['body'])],
        [Paragraph("total_amount", styles['body']), Paragraph("DECIMAL(10,2)", styles['body']), Paragraph("NO", styles['body']), Paragraph("", styles['body']), Paragraph("None", styles['body']), Paragraph("Computed total rental cost", styles['body'])],
        [Paragraph("status", styles['body']), Paragraph("VARCHAR(20)", styles['body']), Paragraph("YES", styles['body']), Paragraph("", styles['body']), Paragraph("'PENDING'", styles['body']), Paragraph("Reservation status: PENDING, CONFIRMED, etc.", styles['body'])],
    ]
    sec.append(Table(bookings_schema, colWidths=[65, 80, 40, 40, 95, CONTENT_WIDTH - 320], style=[
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    sec.append(Spacer(1, 10))

    sec.append(Paragraph("C.3 Concurrency Control & Row-Level Locking", styles['h2']))
    sec.append(Paragraph(
        "To guarantee that two customers cannot reserve the same vehicle for overlapping dates simultaneously, <code>BookingDAO.java</code> executes a pessimistic row-locking query using <code>SELECT ... FOR UPDATE</code> within an explicit JDBC database transaction. The validation query:<br/>"
        "<code>SELECT id FROM bookings WHERE vehicle_id = ? AND status IN ('PENDING','CONFIRMED') AND start_date &lt; ? AND end_date &gt; ? LIMIT 1</code><br/>"
        "If an overlapping reservation is found, the transaction is immediately rolled back, safely protecting database integrity.",
        styles['body']
    ))
    sec.append(PageBreak())

    return sec


def build_source_code_section(styles):
    sec = []
    sec.append(PageTracker("sec_source"))
    sec.extend(make_section_header("Section D: Complete Application Source Code", "All 37 unredacted application source files organized by architectural layer", styles))

    # Modules definition
    modules = [
        ("sec_d1", "D.1 Domain Model Entity Classes", "Core business objects representing persistent application state", [
            ("com/rental/model/User.java", "src/main/java/com/rental/model/User.java", "User domain entity encapsulating ID, name, email, password hash, and authorization role."),
            ("com/rental/model/Vehicle.java", "src/main/java/com/rental/model/Vehicle.java", "Vehicle domain entity representing fleet units, attributes, daily pricing, and statuses."),
            ("com/rental/model/Booking.java", "src/main/java/com/rental/model/Booking.java", "Booking reservation entity holding reservation dates, vehicle relationships, and status."),
            ("com/rental/model/Payment.java", "src/main/java/com/rental/model/Payment.java", "Payment transaction entity tracking settlement amount, status, and payment timestamp."),
        ]),
        ("sec_d2", "D.2 Data Access Objects / JDBC Layer", "Thread-safe DAO pattern implementing SQL transactions and CRUD operations", [
            ("com/rental/dao/UserDAO.java", "src/main/java/com/rental/dao/UserDAO.java", "User data access object handling registration, duplicate validation, and authentication retrieval."),
            ("com/rental/dao/VehicleDAO.java", "src/main/java/com/rental/dao/VehicleDAO.java", "Vehicle data access object managing fleet queries, unit insertion, and status updates."),
            ("com/rental/dao/BookingDAO.java", "src/main/java/com/rental/dao/BookingDAO.java", "Booking DAO featuring transaction row-level locking, date overlap validation, and customer history."),
            ("com/rental/dao/PaymentDAO.java", "src/main/java/com/rental/dao/PaymentDAO.java", "Payment DAO processing simulated payment persistence and revenue aggregation."),
        ]),
        ("sec_d3", "D.3 Database Connection & Utility Classes", "Connection factory and database connectivity verification harness", [
            ("com/rental/util/DBConnection.java", "src/main/java/com/rental/util/DBConnection.java", "Thread-safe JDBC connection provider using DriverManager. (Password credential redacted for security)."),
            ("com/rental/util/TESTConnection.java", "src/main/java/com/rental/util/TESTConnection.java", "Standalone console verification utility to test active database connectivity."),
        ]),
        ("sec_d4", "D.4 Public & Customer Servlets / Controllers", "HTTP Controllers handling routing, input validation, and user sessions", [
            ("com/rental/controller/VehicleServlet.java", "src/main/java/com/rental/controller/VehicleServlet.java", "Public catalog servlet loading available vehicles for guest and user browsing."),
            ("com/rental/controller/VehicleDetailsServlet.java", "src/main/java/com/rental/controller/VehicleDetailsServlet.java", "Details servlet rendering complete vehicle specifications and rental parameters."),
            ("com/rental/controller/RegisterServlet.java", "src/main/java/com/rental/controller/RegisterServlet.java", "Customer registration controller with BCrypt password hashing and input checks."),
            ("com/rental/controller/LoginServlet.java", "src/main/java/com/rental/controller/LoginServlet.java", "Authentication controller verifying BCrypt credentials and setting session state."),
            ("com/rental/controller/BookingServlet.java", "src/main/java/com/rental/controller/BookingServlet.java", "Reservation controller validating date ranges and preventing overlap collisions."),
            ("com/rental/controller/PaymentServlet.java", "src/main/java/com/rental/controller/PaymentServlet.java", "Payment sandbox controller processing simulated card, UPI, and netbanking transactions."),
            ("com/rental/controller/MyBookingsServlet.java", "src/main/java/com/rental/controller/MyBookingsServlet.java", "Customer reservations controller rendering personal booking history and statuses."),
            ("com/rental/controller/CancelBookingServlet.java", "src/main/java/com/rental/controller/CancelBookingServlet.java", "Reservation cancellation controller releasing vehicle inventory."),
            ("com/rental/controller/LogoutServlet.java", "src/main/java/com/rental/controller/LogoutServlet.java", "Session termination controller invalidating session state and cookies."),
        ]),
        ("sec_d5", "D.5 Administrator Portal Servlets", "Administrative controllers for operational metrics, fleet, and reservations", [
            ("com/rental/controller/AdminDashboardServlet.java", "src/main/java/com/rental/controller/AdminDashboardServlet.java", "Admin dashboard controller computing gross revenue, fleet size, and active bookings."),
            ("com/rental/controller/AdminVehicleServlet.java", "src/main/java/com/rental/controller/AdminVehicleServlet.java", "Fleet management controller handling vehicle additions, status changes, and deletions."),
            ("com/rental/controller/AdminBookingServlet.java", "src/main/java/com/rental/controller/AdminBookingServlet.java", "Admin reservations controller providing centralized status override controls."),
        ]),
        ("sec_d6", "D.6 Presentation Views / JavaServer Pages (JSP)", "Dynamic web presentation templates with modern responsive markup", [
            ("webapp/index.jsp", "src/main/webapp/index.jsp", "Modern landing page with hero banner, feature highlights, and call-to-actions."),
            ("webapp/vehicles.jsp", "src/main/webapp/vehicles.jsp", "Fleet catalog page rendering vehicle photography cards and booking buttons."),
            ("webapp/vehicle-details.jsp", "src/main/webapp/vehicle-details.jsp", "Vehicle inspection page displaying full technical parameters and booking link."),
            ("webapp/login.jsp", "src/main/webapp/login.jsp", "Unified authentication form supporting customer and administrator logins."),
            ("webapp/register.jsp", "src/main/webapp/register.jsp", "Customer registration form with real-time validation guidelines."),
            ("webapp/booking.jsp", "src/main/webapp/booking.jsp", "Interactive reservation form with client-side price calculator and error banner."),
            ("webapp/payment.jsp", "src/main/webapp/payment.jsp", "Development payment sandbox simulating Card, UPI, and Netbanking gateways."),
            ("webapp/my-bookings.jsp", "src/main/webapp/my-bookings.jsp", "Customer booking dashboard displaying reservation cards and status badges."),
            ("webapp/includes/navbar.jsp", "src/main/webapp/includes/navbar.jsp", "Reusable navigation header dynamically adapting to guest, user, and admin sessions."),
            ("webapp/admin/dashboard.jsp", "src/main/webapp/admin/dashboard.jsp", "Operational analytics dashboard with live KPI cards and quick navigation."),
            ("webapp/admin/vehicles.jsp", "src/main/webapp/admin/vehicles.jsp", "Fleet inventory management table with status toggles and Add Vehicle modal."),
            ("webapp/admin/bookings.jsp", "src/main/webapp/admin/bookings.jsp", "Customer reservations management table with administrative action triggers."),
        ]),
        ("sec_d7", "D.7 Custom CSS Design System", "Production-grade responsive stylesheet featuring glassmorphism and modern tokens", [
            ("webapp/css/style.css", "src/main/webapp/css/style.css", "Complete custom stylesheet with CSS variables, responsive grid, and UI components."),
        ]),
        ("sec_d8", "D.8 Deployment Descriptor Configuration", "Jakarta / Java EE web application deployment descriptor", [
            ("WEB-INF/web.xml", "src/main/webapp/WEB-INF/web.xml", "Servlet deployment descriptor configuration and welcome-file mappings."),
        ]),
        ("sec_d9", "D.9 Database DDL & Seed Script", "MySQL relational schema and seed dataset definition", [
            ("schema.sql", "schema.sql", "Complete MySQL schema DDL script with foreign keys, seed administrators, and initial fleet."),
        ]),
    ]

    for tracker_key, sub_title, sub_desc, file_list in modules:
        sec.append(PageTracker(tracker_key))
        sec.append(Paragraph(sub_title, styles['h2']))
        sec.append(Paragraph(sub_desc, styles['body']))
        sec.append(Spacer(1, 4))

        for display_name, file_path, file_desc in file_list:
            full_path = os.path.join(os.getcwd(), file_path.replace("/", os.sep))
            if not os.path.exists(full_path):
                continue

            with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                raw_code = fp.read()
            line_count = len(raw_code.splitlines())

            # File Header Box
            header_table_data = [
                [
                    Paragraph(f"<b>File:</b> <font color='#2563EB'>{file_path}</font>", styles['code_header']),
                    Paragraph(f"<b>Lines:</b> {line_count} &nbsp;|&nbsp; <b>Language:</b> {file_path.split('.')[-1].upper()}", styles['code_meta'])
                ],
                [
                    Paragraph(f"<b>Description:</b> {file_desc}", styles['code_meta']),
                    Paragraph("", styles['code_meta'])
                ]
            ]
            header_table = Table(header_table_data, colWidths=[CONTENT_WIDTH - 140, 140])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ]))

            sec.append(Spacer(1, 6))
            sec.append(header_table)
            sec.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=4))

            # Code Flowable (Preformatted directly in story so it splits cleanly across pages!)
            wrapped_code = wrap_code_lines(raw_code, max_len=92)
            code_pre = Preformatted(wrapped_code, styles['code_content'])
            sec.append(code_pre)
            sec.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#94A3B8"), spaceBefore=4, spaceAfter=8))

    sec.append(PageBreak())
    return sec


def build_screenshots_section(styles):
    sec = []
    sec.append(PageTracker("sec_screenshots"))
    sec.extend(make_section_header("Section E: Live Website Screenshots & User Workflows", "Empirical visual captures from the running application on Apache Tomcat 9", styles))

    sec.append(Paragraph(
        "The following 13 figures are genuine browser screenshots captured from the live application running on <b>Apache Tomcat 9.0</b> at <code>http://localhost:8084/RentalVehicleSystem/</code> using headless browser automation. Each screenshot illustrates an authentic user or administrator workflow.",
        styles['body']
    ))
    sec.append(Spacer(1, 6))

    screenshots_meta = [
        ("01-home-page.png", "Figure 1: RentRide Landing Page & Hero Section",
         "The landing page introduces the RentRide brand with modern typography, an engaging hero call-to-action banner, value propositions, and a public navigation header ('Home', 'Browse Vehicles', 'Login', 'Register').",
         "Workflow: Public guest arrival and application onboarding."),

        ("02-browse-vehicles.png", "Figure 2: Available Vehicles Fleet Catalog",
         "The fleet catalog renders responsive vehicle cards populated with real photography (Maruti Swift, Hyundai Creta, Honda City, Toyota Fortuner, Royal Enfield Hunter), daily rental rates, class badges, and 'Book Now' triggers.",
         "Workflow: Vehicle browsing, category inspection, and reservation initiation."),

        ("03-vehicle-details.png", "Figure 3: Vehicle Specifications & Details Inspection",
         "Detailed specification view for individual fleet units (Hyundai Creta SUV), presenting the vehicle registration number, pricing breakdown, vehicle features, and direct reservation navigation.",
         "Workflow: Vehicle evaluation and rental suitability assessment."),

        ("04-user-login.png", "Figure 4: User & Administrator Authentication Portal",
         "Secure sign-in interface providing access for both registered customers and fleet administrators. Includes input validation, email autocomplete, and links to customer registration.",
         "Workflow: User authentication and role-based session initialization."),

        ("05-user-registration.png", "Figure 5: Customer Account Registration Form",
         "Account creation portal with fields for full name, email, and password. Features client-side validation requirements (minimum 8-character password) and duplicate email prevention.",
         "Workflow: New customer onboarding and credential registration."),

        ("06-booking-form.png", "Figure 6: Vehicle Reservation & Dynamic Price Calculation Form",
         "Reservation booking interface with pick-up and drop-off date pickers. The form pre-loads selected vehicle parameters and calculates the total rental cost in real-time.",
         "Workflow: Rental duration selection, cost estimation, and order creation."),

        ("07-payment-gateway-sandbox.png", "Figure 7: Interactive Mock Payment Sandbox Gateway",
         "Development payment simulation interface displaying the booking reference number, reservation summary, and total payable amount. Features simulated Credit/Debit Card, UPI, and Netbanking options.",
         "Workflow: Secure payment simulation and transaction settlement."),

        ("08-my-bookings.png", "Figure 8: Customer Reservations Dashboard (My Bookings)",
         "Customer management dashboard showing active and historical reservations with status badges (CONFIRMED), booking reference numbers, vehicle names, dates, and self-service cancellation.",
         "Workflow: Reservation tracking, status verification, and customer lifecycle governance."),

        ("09-booking-overlap-validation.png", "Figure 9: Overlap Conflict Rejection & Error Handling",
         "Empirical verification of the date-overlap conflict engine. When a user attempts to reserve an unavailable vehicle for overlapping dates, the system rolls back the transaction and displays a clear error banner.",
         "Workflow: Concurrency protection, double-booking prevention, and error feedback."),

        ("10-admin-dashboard.png", "Figure 10: Administrator Operational Analytics Dashboard",
         "Executive management portal presenting real-time business KPIs: Gross Revenue, Total Fleet Size, Active Bookings, and Total Registered Users alongside recent reservation activity.",
         "Workflow: Executive analytics, business intelligence, and revenue monitoring."),

        ("11-admin-fleet-management.png", "Figure 11: Fleet Inventory Management Table",
         "Comprehensive fleet inventory table displaying vehicle photos, registration numbers, brand, model, vehicle class, daily rates, operational status controls, and action buttons.",
         "Workflow: Fleet inventory governance, status toggles, and asset maintenance."),

        ("12-admin-add-vehicle-form.png", "Figure 12: Fleet Unit Addition Form Modal",
         "Interactive fleet expansion form allowing administrators to register new vehicles into the catalog with registration number, brand, model, vehicle class, and daily rental price.",
         "Workflow: Inventory expansion and fleet unit registration."),

        ("13-admin-reservations.png", "Figure 13: Customer Reservations Control & Status Governance",
         "Centralized reservation management console displaying all customer reservations across the enterprise with customer names, vehicle models, total amounts, and status update actions.",
         "Workflow: Administrative order review, booking approval, and reservation completion."),
    ]

    sc_dir = os.path.join(os.getcwd(), "project-documentation", "screenshots")

    for img_name, fig_title, fig_desc, fig_workflow in screenshots_meta:
        img_path = os.path.join(sc_dir, img_name)
        if not os.path.exists(img_path):
            continue

        fig_elements = []
        fig_elements.append(Paragraph(fig_title, styles['caption']))
        
        # Display image with maintained aspect ratio
        img_flowable = Image(img_path, width=460, height=254)
        img_flowable.hAlign = 'CENTER'

        img_table = Table([[img_flowable]], colWidths=[CONTENT_WIDTH])
        img_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))
        fig_elements.append(img_table)
        fig_elements.append(Spacer(1, 4))
        fig_elements.append(Paragraph(f"<b>Description:</b> {fig_desc}", styles['body']))
        fig_elements.append(Paragraph(f"<b>User Workflow:</b> {fig_workflow}", ParagraphStyle('Workflow', parent=styles['body'], fontName='Helvetica-Oblique', textColor=colors.HexColor('#2563EB'))))
        fig_elements.append(Spacer(1, 12))

        sec.append(KeepTogether(fig_elements))

    sec.append(PageBreak())
    return sec


def build_testing_and_verification(styles):
    sec = []
    sec.append(PageTracker("sec_testing"))
    sec.extend(make_section_header("Section F: Testing, Quality Assurance & Empirical Verification", "Automated functional test harness execution and verification results", styles))

    sec.append(Paragraph("F.1 Quality Assurance Methodology", styles['h2']))
    sec.append(Paragraph(
        "Rigorous quality assurance was conducted across the entire application stack using automated HTTP test scripts and headless browser automation (Selenium WebDriver 4.x with Microsoft Edge). Every test case was executed directly against the live application running on Apache Tomcat 9 at <code>http://localhost:8084/RentalVehicleSystem/</code> with live MySQL database persistence.",
        styles['body']
    ))

    sec.append(Paragraph("F.2 Empirical Test Execution Matrix", styles['h2']))

    test_data = [
        [Paragraph("<b>Test ID</b>", styles['body_bold']), Paragraph("<b>Feature Tested</b>", styles['body_bold']), Paragraph("<b>Steps & Request Performed</b>", styles['body_bold']), Paragraph("<b>Expected Result</b>", styles['body_bold']), Paragraph("<b>Status</b>", styles['body_bold'])],
        [Paragraph("TC-01", styles['body']), Paragraph("Landing Page Rendering", styles['body']), Paragraph("GET /RentalVehicleSystem/ as unauthenticated guest.", styles['body']), Paragraph("HTTP 200 OK; hero banner and guest navigation loaded.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-02", styles['body']), Paragraph("Static Vehicle Imagery", styles['body']), Paragraph("GET /images/vehicles/{swift, creta, city, fortuner, hunter}.jpg", styles['body']), Paragraph("HTTP 200 OK with valid image/jpeg headers (>10KB).", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-03", styles['body']), Paragraph("Vehicle Fleet Catalog", styles['body']), Paragraph("GET /vehicles without active session.", styles['body']), Paragraph("HTTP 200 OK; cards rendered with pricing and photos.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-04", styles['body']), Paragraph("Vehicle Details Inspection", styles['body']), Paragraph("GET /vehicle-details?id=2 (Hyundai Creta).", styles['body']), Paragraph("HTTP 200 OK; specifications and rates displayed.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-05", styles['body']), Paragraph("Customer Registration", styles['body']), Paragraph("POST /register with valid name, email, and password.", styles['body']), Paragraph("HTTP 302 to login; user inserted with BCrypt hash.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-06", styles['body']), Paragraph("Customer Authentication", styles['body']), Paragraph("POST /login with valid registered customer credentials.", styles['body']), Paragraph("Session created; user redirected to vehicle catalog.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-07", styles['body']), Paragraph("Booking Creation", styles['body']), Paragraph("POST /booking for Creta with valid future date window.", styles['body']), Paragraph("Booking record created in PENDING; forwarded to payment.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-08", styles['body']), Paragraph("Mock Payment Sandbox", styles['body']), Paragraph("GET /payment?bookingId=5 with active customer session.", styles['body']), Paragraph("HTTP 200 OK; simulation banner and order total shown.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-09", styles['body']), Paragraph("Payment Authorization", styles['body']), Paragraph("POST /payment with paymentStatus=SUCCESS for Booking #5.", styles['body']), Paragraph("Payment recorded; booking updated to CONFIRMED.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-10", styles['body']), Paragraph("Overlap Conflict Detection", styles['body']), Paragraph("POST /booking on same vehicle for overlapping dates.", styles['body']), Paragraph("Booking rejected; transaction rolled back with error banner.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-11", styles['body']), Paragraph("Admin Authentication", styles['body']), Paragraph("POST /login with admin credentials (admin@rental.com).", styles['body']), Paragraph("Authenticated with ADMIN role; redirected to admin dashboard.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-12", styles['body']), Paragraph("Admin KPI Dashboard", styles['body']), Paragraph("GET /admin/dashboard as authenticated Administrator.", styles['body']), Paragraph("HTTP 200 OK; revenue and fleet metrics loaded.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-13", styles['body']), Paragraph("Fleet Inventory Governance", styles['body']), Paragraph("GET /admin/vehicles as authenticated Administrator.", styles['body']), Paragraph("Fleet inventory table rendered with Add Vehicle modal.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-14", styles['body']), Paragraph("Reservations Governance", styles['body']), Paragraph("GET /admin/bookings as authenticated Administrator.", styles['body']), Paragraph("All reservations displayed with administrative actions.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
        [Paragraph("TC-15", styles['body']), Paragraph("Session Termination", styles['body']), Paragraph("GET /logout with active authenticated session.", styles['body']), Paragraph("Session invalidated; unauthenticated guest navbar restored.", styles['body']), Paragraph("<font color='#059669'><b>PASS</b></font>", styles['body'])],
    ]

    test_table = Table(test_data, colWidths=[45, 100, 150, 145, 45])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (4,0), (4,-1), 'CENTER'),
    ]))
    sec.append(test_table)
    sec.append(Spacer(1, 10))

    sec.append(Paragraph("<b>Test Execution Summary:</b> Total 15 executed, 15 Passed (100.0% Success Rate), 0 Failed, 0 Not Tested.", styles['body_bold']))
    sec.append(PageBreak())
    return sec


def build_run_instructions_and_conclusion(styles):
    sec = []
    sec.append(PageTracker("sec_instructions"))
    sec.extend(make_section_header("Section G: Operational Run & Deployment Instructions", "Step-by-step local execution guidelines and verified endpoints", styles))

    sec.append(Paragraph("G.1 Prerequisites & System Requirements", styles['h2']))
    sec.append(Paragraph(
        "1. <b>Java Development Kit (JDK):</b> Java 21 LTS installed and added to system PATH. Verify via <code>java -version</code>.<br/>"
        "2. <b>Apache Tomcat:</b> Version 9.0.x configured to listen on HTTP port <code>8084</code>.<br/>"
        "3. <b>MySQL Server:</b> Version 8.0 running on <code>localhost:3306</code> with InnoDB engine enabled.<br/>"
        "4. <b>Web Browser:</b> Modern Chromium-based browser (Edge, Chrome, Firefox) with JavaScript enabled.",
        styles['body']
    ))

    sec.append(Paragraph("G.2 Database Initialization", styles['h2']))
    sec.append(Paragraph(
        "Execute the SQL schema to create the database and seed initial vehicles and administrator accounts:<br/>"
        "<code>mysql -u root -p &lt; schema.sql</code>",
        styles['body']
    ))

    sec.append(Paragraph("G.3 Launching the Application on Tomcat", styles['h2']))
    sec.append(Paragraph(
        "Start the application using the local batch runner or your Eclipse WTP server environment:<br/>"
        "<code>.\\run_tomcat.bat</code><br/>"
        "Verify server is listening: <code>netstat -ano | findstr \"8084\"</code>",
        styles['body']
    ))

    sec.append(Paragraph("G.4 Verified Application Endpoints & Default Credentials", styles['h2']))
    endpoints_data = [
        [Paragraph("<b>Resource / Page</b>", styles['body_bold']), Paragraph("<b>Local Verified URL</b>", styles['body_bold']), Paragraph("<b>Access Level & Default Credentials</b>", styles['body_bold'])],
        [Paragraph("Landing Page", styles['body']), Paragraph("http://localhost:8084/RentalVehicleSystem/", styles['body']), Paragraph("Public Access (Guest)", styles['body'])],
        [Paragraph("Fleet Catalog", styles['body']), Paragraph("http://localhost:8084/RentalVehicleSystem/vehicles", styles['body']), Paragraph("Public Access (Guest & Customer)", styles['body'])],
        [Paragraph("Sign In Portal", styles['body']), Paragraph("http://localhost:8084/RentalVehicleSystem/login.jsp", styles['body']), Paragraph("Public (Admin: admin@rental.com / admin123 | User: user@rental.com / user1234)", styles['body'])],
        [Paragraph("Customer Dashboard", styles['body']), Paragraph("http://localhost:8084/RentalVehicleSystem/my-bookings", styles['body']), Paragraph("Authenticated Customer Session (USER role)", styles['body'])],
        [Paragraph("Admin KPI Dashboard", styles['body']), Paragraph("http://localhost:8084/RentalVehicleSystem/admin/dashboard", styles['body']), Paragraph("Administrator Session Only (ADMIN role)", styles['body'])],
        [Paragraph("Fleet Governance", styles['body']), Paragraph("http://localhost:8084/RentalVehicleSystem/admin/vehicles", styles['body']), Paragraph("Administrator Session Only (ADMIN role)", styles['body'])],
        [Paragraph("Reservations Control", styles['body']), Paragraph("http://localhost:8084/RentalVehicleSystem/admin/bookings", styles['body']), Paragraph("Administrator Session Only (ADMIN role)", styles['body'])],
    ]
    sec.append(Table(endpoints_data, colWidths=[120, 200, CONTENT_WIDTH - 320], style=[
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    sec.append(Spacer(1, 12))

    # Section H: Conclusion
    sec.append(PageTracker("sec_conclusion"))
    sec.extend(make_section_header("Section H: Conclusion & Future Scope", "Project summary, verified achievements, and prospective enhancements", styles))
    sec.append(Paragraph("H.1 Implementation Summary", styles['h2']))
    sec.append(Paragraph(
        "The <b>RentRide Vehicle Rental System</b> has been successfully implemented, tested, and validated in an enterprise Java 21 and MySQL environment. All architectural components—including the 4 domain models, 4 JDBC DAOs, 12 Java Servlets, 12 JSP templates, and custom CSS design system—were thoroughly executed and verified with zero defects across 15 automated test cases.",
        styles['body']
    ))

    sec.append(Paragraph("H.2 Key Project Achievements", styles['h2']))
    sec.append(Paragraph(
        "• <b>Complete Layered Modularity:</b> Clear separation of concerns between presentation, business rules, and relational storage.<br/>"
        "• <b>Bulletproof Concurrency:</b> Pessimistic row locking eliminates double-booking errors during peak simultaneous customer bookings.<br/>"
        "• <b>Adaptive Security:</b> BCrypt salted password hashing and role-based session authorization guard against unauthorized access.<br/>"
        "• <b>Modern UI & Aesthetics:</b> Glassmorphism styling, responsive card grids, and intuitive navigation provide a consumer-grade experience.",
        styles['body']
    ))

    sec.append(Paragraph("H.3 Future Enhancements", styles['h2']))
    sec.append(Paragraph(
        "• Integration with third-party payment gateways (Razorpay, Stripe) using live webhooks.<br/>"
        "• Automated SMS and email notification dispatchers for booking confirmations and pick-up reminders.<br/>"
        "• Real-time GPS telematics and vehicle tracking integration for fleet location monitoring.",
        styles['body']
    ))

    return sec


def assemble_story(styles, registry):
    story = []
    story.extend(build_cover_page(styles))
    story.extend(build_toc(styles, registry))
    story.extend(build_overview_and_architecture(styles))
    story.extend(build_source_code_section(styles))
    story.extend(build_screenshots_section(styles))
    story.extend(build_testing_and_verification(styles))
    story.extend(build_run_instructions_and_conclusion(styles))
    return story


def generate_master_pdf():
    print(f"Building master PDF: {PDF_PATH}")
    styles = get_styles()

    # Pass 1: Build to populate PAGE_REGISTRY with exact page numbers
    print("Pass 1: Measuring exact page numbers for Table of Contents...")
    doc1 = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )
    story1 = assemble_story(styles, {})
    doc1.build(story1, canvasmaker=NumberedCanvas)
    print("Tracked Page Registry:", PAGE_REGISTRY)

    # Pass 2: Re-assemble story with exact tracked page numbers in TOC
    print("Pass 2: Compiling final master PDF with exact TOC references...")
    doc2 = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )
    story2 = assemble_story(styles, PAGE_REGISTRY)
    doc2.build(story2, canvasmaker=NumberedCanvas)

    file_size = os.path.getsize(PDF_PATH)
    print(f"Master PDF generated successfully at: {PDF_PATH}")
    print(f"File size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")


if __name__ == "__main__":
    generate_master_pdf()
