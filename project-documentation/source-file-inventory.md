# Source File Inventory: Vehicle Rental System (RentRide)

This document provides a comprehensive audit of all source code files comprising the **Vehicle Rental System (RentRide)** web application, detailing the files included in the official project documentation and PDF report, alongside files intentionally excluded with corresponding technical rationales.

---

## 1. Summary Statistics

| Category | Count | Primary Technology |
| :--- | :---: | :--- |
| **Database Schema & Seeds** | 1 | SQL (MySQL 8.0 DDL & DML) |
| **Java Domain Models** | 4 | Java 21 POJO / Entity Classes |
| **Java Data Access Objects (DAO)** | 4 | Java 21 JDBC PreparedStatement DAOs |
| **Java Utility & Connection Classes** | 2 | JDBC Connection Manager & Verification |
| **Java Servlets (Public & Customer)** | 9 | Jakarta/Java EE Servlets (Controller Layer) |
| **Java Servlets (Admin Management)** | 3 | Admin Operations & Dashboard Controllers |
| **Web Views (JSP Pages)** | 12 | JavaServer Pages (Presentation Layer) |
| **Web Application Stylesheet** | 1 | Vanilla Modern CSS3 Design System |
| **Deployment Descriptor** | 1 | XML (`web.xml` Web Application Config) |
| **Total Included Source Files** | **37** | **Complete Application Source Code** |

---

## 2. Included Source Files (Full Application Scope)

### A. Database Layer
| # | Relative File Path | Language | Lines | Description & Purpose |
| :-: | :--- | :--- | :-: | :--- |
| 1 | `schema.sql` | SQL | 70 | MySQL schema creating `users`, `vehicles`, `bookings`, `payments` tables with constraints and default seeds. |

### B. Domain Model / Entity Layer (`com.rental.model`)
| # | Relative File Path | Language | Lines | Description & Purpose |
| :-: | :--- | :--- | :-: | :--- |
| 2 | `src/main/java/com/rental/model/User.java` | Java | 61 | User entity encapsulating user ID, name, email, password hash, and role (USER / ADMIN). |
| 3 | `src/main/java/com/rental/model/Vehicle.java` | Java | 100 | Vehicle entity representing fleet inventory, brand, model, class, daily rate, and status. |
| 4 | `src/main/java/com/rental/model/Booking.java` | Java | 121 | Booking reservation entity holding dates, vehicle association, computed totals, and statuses. |
| 5 | `src/main/java/com/rental/model/Payment.java` | Java | 63 | Payment transaction record with amount, payment status, timestamp, and booking link. |

### C. Data Access Object (DAO) Layer (`com.rental.dao`)
| # | Relative File Path | Language | Lines | Description & Purpose |
| :-: | :--- | :--- | :-: | :--- |
| 6 | `src/main/java/com/rental/dao/UserDAO.java` | Java | 84 | CRUD operations for user registration, duplicate email verification, and retrieval. |
| 7 | `src/main/java/com/rental/dao/VehicleDAO.java` | Java | 162 | Fleet queries, vehicle insertion, status updates, rate editing, and deletion. |
| 8 | `src/main/java/com/rental/dao/BookingDAO.java` | Java | 273 | Booking creation with overlap validation, status transitions, and customer history retrieval. |
| 9 | `src/main/java/com/rental/dao/PaymentDAO.java` | Java | 108 | Payment persistence, booking status confirmation, and revenue calculation. |

### D. Utility & Connection Layer (`com.rental.util`)
| # | Relative File Path | Language | Lines | Description & Purpose |
| :-: | :--- | :--- | :-: | :--- |
| 10 | `src/main/java/com/rental/util/DBConnection.java` | Java | 21 | Thread-safe MySQL JDBC connection factory using `DriverManager`. *(Credentials redacted in PDF)* |
| 11 | `src/main/java/com/rental/util/TESTConnection.java` | Java | 17 | Standalone console test harness to verify database connectivity. |

### E. Controller / Servlet Layer (`com.rental.controller`)
| # | Relative File Path | Language | Lines | Description & Purpose |
| :-: | :--- | :--- | :-: | :--- |
| 12 | `src/main/java/com/rental/controller/VehicleServlet.java` | Java | 28 | Handles `/vehicles` catalog route, fetching available inventory. |
| 13 | `src/main/java/com/rental/controller/VehicleDetailsServlet.java` | Java | 39 | Handles `/vehicle-details` route for individual vehicle specs. |
| 14 | `src/main/java/com/rental/controller/RegisterServlet.java` | Java | 58 | Handles user account registration with BCrypt hashing and email uniqueness checks. |
| 15 | `src/main/java/com/rental/controller/LoginServlet.java` | Java | 60 | Handles user and admin authentication, session initialization, and role-based redirection. |
| 16 | `src/main/java/com/rental/controller/BookingServlet.java` | Java | 134 | Validates date ranges, calculates rental totals, and prevents overlapping reservations. |
| 17 | `src/main/java/com/rental/controller/PaymentServlet.java` | Java | 135 | Processes mock sandbox payments, updates booking confirmation, and inserts payments. |
| 18 | `src/main/java/com/rental/controller/MyBookingsServlet.java` | Java | 35 | Renders customer booking history with status badges. |
| 19 | `src/main/java/com/rental/controller/CancelBookingServlet.java` | Java | 50 | Allows users/admins to cancel reservations and release fleet units. |
| 20 | `src/main/java/com/rental/controller/LogoutServlet.java` | Java | 31 | Invalidate customer/admin session and redirect to landing page. |
| 21 | `src/main/java/com/rental/controller/AdminDashboardServlet.java` | Java | 51 | Computes revenue, total fleet, active reservations, and user metrics for admin view. |
| 22 | `src/main/java/com/rental/controller/AdminVehicleServlet.java` | Java | 135 | Admin fleet inventory controls (add new vehicle, update status, delete unit). |
| 23 | `src/main/java/com/rental/controller/AdminBookingServlet.java` | Java | 58 | Admin reservation management (approve, confirm, cancel, view all orders). |

### F. Presentation Layer (JSP & Views)
| # | Relative File Path | Language | Lines | Description & Purpose |
| :-: | :--- | :--- | :-: | :--- |
| 24 | `src/main/webapp/index.jsp` | JSP | 54 | Modern landing page with hero banner, call-to-actions, and value propositions. |
| 25 | `src/main/webapp/vehicles.jsp` | JSP | 76 | Vehicle catalog page displaying responsive cards with photography and pricing. |
| 26 | `src/main/webapp/vehicle-details.jsp` | JSP | 70 | Vehicle specifications and direct booking navigation. |
| 27 | `src/main/webapp/login.jsp` | JSP | 61 | Clean sign-in form supporting both customer and administrator credentials. |
| 28 | `src/main/webapp/register.jsp` | JSP | 60 | User sign-up form with password validation rules. |
| 29 | `src/main/webapp/booking.jsp` | JSP | 121 | Interactive reservation form with real-time price calculation and error alerts. |
| 30 | `src/main/webapp/payment.jsp` | JSP | 114 | Mock payment sandbox simulating Card, UPI, and Netbanking gateways. |
| 31 | `src/main/webapp/my-bookings.jsp` | JSP | 127 | Customer dashboard with reservation cards, statuses, and cancellation controls. |
| 32 | `src/main/webapp/includes/navbar.jsp` | JSP | 44 | Reusable navigation header dynamically adapting to guest, user, and admin sessions. |
| 33 | `src/main/webapp/admin/dashboard.jsp` | JSP | 125 | Operational administration dashboard with analytics cards and quick links. |
| 34 | `src/main/webapp/admin/vehicles.jsp` | JSP | 210 | Fleet inventory management table with status toggles and modal form. |
| 35 | `src/main/webapp/admin/bookings.jsp` | JSP | 111 | Reservation management table with administrative action triggers. |

### G. Styling & Deployment Configuration
| # | Relative File Path | Language | Lines | Description & Purpose |
| :-: | :--- | :--- | :-: | :--- |
| 36 | `src/main/webapp/css/style.css` | CSS | 1068 | Complete custom modern CSS design system, responsive grid, glassmorphism, and buttons. |
| 37 | `src/main/webapp/WEB-INF/web.xml` | XML | 21 | Web application deployment descriptor configuration. |

---

## 3. Intentionally Excluded Files

| File / Directory Path | Classification | Technical Rationale for Exclusion |
| :--- | :--- | :--- |
| `.classpath`, `.project`, `.settings/` | IDE Configuration | Eclipse workspace metadata; not part of the runtime software logic. |
| `build/classes/**` | Compiled Binaries | Java `.class` bytecode generated during compilation; represented by corresponding `.java` source files. |
| `src/main/webapp/WEB-INF/classes/**` | Compiled Binaries | Web application deployed class binaries; redundant with Java source files. |
| `src/main/webapp/WEB-INF/lib/*.jar` | Third-Party Libraries | Precompiled JAR dependencies (`mysql-connector-j-26.7.0.jar`, `jbcrypt-0.4.jar`, `ojdbc14.jar`); documented in Architecture and Run Instructions. |
| `src/main/webapp/images/vehicles/*.jpg` | Binary Media | Vehicle photography JPEG assets; captured visually and demonstrated through real browser screenshots in Section 3 and Section F of the PDF. |
| `lbrce_logo.jpeg` | Binary Media | College insignia used for documentation cover page. |
| `run_tomcat.bat` | Helper Script | Local execution launcher used for background daemon deployment during verification. |
| `tomcat_out.log`, `tomcat_err.log` | Ephemeral Logs | Temporary server standard output and diagnostic logs. |
| `capture_screenshots.py` | Automation Tool | Selenium WebDriver script utilized to automate headless browser capture. |
| `test_rental_system.py` | Test Automation | Automated test harness; results and assertions fully documented in `test-results.md`. |
| `generate_academic_report.py` | Legacy Generator | Previous Word report generation script; superseded by the comprehensive PDF documentation generator. |
