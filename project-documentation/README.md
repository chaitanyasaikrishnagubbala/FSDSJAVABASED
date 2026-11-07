# RentRide — Vehicle Rental System

A full-stack, enterprise-grade Vehicle Rental Web Application built with **Java 21**, **Java Servlets**, **JavaServer Pages (JSP)**, **JDBC**, **MySQL 8.0**, and **Apache Tomcat 9.0**.

---

## 1. Project Overview

**RentRide** streamlines the vehicle rental ecosystem for both customers and fleet administrators:
- **Customers** can browse available vehicles (Hatchbacks, Sedans, SUVs, Motorcycles), inspect vehicle details, reserve rental dates, simulate payments through a dedicated test sandbox, and view or cancel bookings.
- **Fleet Administrators** can monitor operational analytics (gross revenue, active reservations, fleet utilization), manage inventory (add vehicles, update rental rates, toggle availability), and manage customer bookings.

---

## 2. Technology Stack

- **Backend Runtime:** Java 21 (OpenJDK 64-Bit Server VM)
- **Web & Servlet Container:** Apache Tomcat 9.0.120
- **Database Engine:** MySQL Server 8.0 (Port 3306)
- **Persistence Layer:** Java Database Connectivity (JDBC) with thread-safe `PreparedStatement` and row-level transaction locking
- **Cryptography:** BCrypt (jBCrypt 0.4) for adaptive salted password hashing
- **Frontend / UI:** JSP, Vanilla CSS3 (Custom Glassmorphism Design System, CSS Variables, Flexbox/Grid), JavaScript
- **Testing & Automation:** Python 3.13, Selenium WebDriver 4.x, Headless Microsoft Edge

---

## 3. Prerequisites & Environment Setup

1. **Java Development Kit (JDK):** Version 21 or higher. Verify with `java -version`.
2. **Apache Tomcat:** Version 9.0.x configured to listen on HTTP port `8084` (configured in `conf/server.xml`).
3. **MySQL Server:** Version 8.0 running on localhost port `3306`.
4. **Python:** Version 3.10+ (for documentation generation and test automation).
   ```bash
   pip install selenium pillow reportlab
   ```

---

## 4. Database Setup & Initialization

1. Start the MySQL service.
2. Execute the provided database schema script:
   ```bash
   mysql -u root -p < schema.sql
   ```
3. The script creates the database `rental_vehicle` and four relational tables:
   - `users`: Customer and administrator authentication records.
   - `vehicles`: Fleet inventory with vehicle attributes, registration numbers, and rental rates.
   - `bookings`: Reservation records with date ranges, total amounts, and statuses.
   - `payments`: Mock transaction logs linked to bookings.
4. Default seed accounts included:
   - **Administrator:** `admin@rental.com` / `admin123`
   - **Customer:** `user@rental.com` / `user1234`

---

## 5. Running the Application Locally

### A. Deploy to Tomcat
Ensure the application is deployed with the context path `/RentalVehicleSystem`:
- **Eclipse WTP Deployment:** Point Tomcat to `RentalVehicleSystem` project folder or `wtpwebapps/RentalVehicleSystem`.
- **Manual WAR Deployment:** Build and copy `RentalVehicleSystem.war` to Tomcat's `webapps/` directory.

### B. Start Apache Tomcat
Start Tomcat via command line or IDE:
```powershell
# Using the provided runtime launcher:
.\run_tomcat.bat
```
Verify Tomcat is listening on port `8084`:
```powershell
netstat -ano | findstr "8084"
```

### C. Access the Website
Open your browser and navigate to:
- **Landing Page:** `http://localhost:8084/RentalVehicleSystem/`
- **Browse Fleet:** `http://localhost:8084/RentalVehicleSystem/vehicles`
- **Sign In:** `http://localhost:8084/RentalVehicleSystem/login.jsp`
- **Register:** `http://localhost:8084/RentalVehicleSystem/register.jsp`
- **Admin Dashboard:** `http://localhost:8084/RentalVehicleSystem/admin/dashboard`

---

## 6. Project Directory Structure

```text
RentalVehicleSystem/
│
├── schema.sql                              # MySQL DDL schema and initial seed data
├── run_tomcat.bat                          # Local Tomcat execution launcher
├── test_rental_system.py                   # Automated functional test suite
├── capture_screenshots.py                  # Headless browser screenshot capture script
│
├── src/main/java/com/rental/
│   ├── model/                              # Domain Entity classes
│   │   ├── User.java
│   │   ├── Vehicle.java
│   │   ├── Booking.java
│   │   └── Payment.java
│   ├── dao/                                # Data Access Objects (JDBC)
│   │   ├── UserDAO.java
│   │   ├── VehicleDAO.java
│   │   ├── BookingDAO.java
│   │   └── PaymentDAO.java
│   ├── controller/                         # Java Servlets (HTTP Handlers)
│   │   ├── VehicleServlet.java
│   │   ├── VehicleDetailsServlet.java
│   │   ├── RegisterServlet.java
│   │   ├── LoginServlet.java
│   │   ├── BookingServlet.java
│   │   ├── PaymentServlet.java
│   │   ├── MyBookingsServlet.java
│   │   ├── CancelBookingServlet.java
│   │   ├── LogoutServlet.java
│   │   ├── AdminDashboardServlet.java
│   │   ├── AdminVehicleServlet.java
│   │   └── AdminBookingServlet.java
│   └── util/                               # Connection Managers
│       ├── DBConnection.java
│       └── TESTConnection.java
│
├── src/main/webapp/
│   ├── index.jsp                           # Public landing page
│   ├── vehicles.jsp                        # Public fleet catalog
│   ├── vehicle-details.jsp                 # Single vehicle details
│   ├── login.jsp                           # Sign-in page
│   ├── register.jsp                        # Sign-up page
│   ├── booking.jsp                         # Reservation booking form
│   ├── payment.jsp                         # Mock payment sandbox
│   ├── my-bookings.jsp                     # Customer bookings dashboard
│   ├── includes/
│   │   └── navbar.jsp                      # Dynamic navigation bar
│   ├── admin/
│   │   ├── dashboard.jsp                   # Admin KPI dashboard
│   │   ├── vehicles.jsp                    # Fleet inventory management
│   │   └── bookings.jsp                    # Customer reservations management
│   ├── css/
│   │   └── style.css                       # Complete CSS design system
│   ├── images/vehicles/                    # Vehicle photography assets
│   └── WEB-INF/
│       ├── web.xml                         # Deployment descriptor
│       └── lib/                            # JDBC & BCrypt JAR libraries
│
└── project-documentation/
    ├── Vehicle_Rental_System_Source_Code_and_Screenshots.pdf # Master Project Documentation PDF
    ├── screenshots/                        # Live application screenshots
    ├── README.md                           # Project instructions and documentation details
    ├── test-results.md                     # Test execution results table
    └── source-file-inventory.md            # Complete audit of project files
```

---

## 7. Generating Documentation & PDF

To re-run automated verification and regenerate the full documentation:
1. Ensure MySQL and Tomcat are running.
2. Run functional tests:
   ```bash
   python test_rental_system.py
   ```
3. Capture live browser screenshots:
   ```bash
   python capture_screenshots.py
   ```
4. Build the master PDF report:
   ```bash
   python generate_pdf.py
   ```
The output PDF is saved to:
`project-documentation/Vehicle_Rental_System_Source_Code_and_Screenshots.pdf`
