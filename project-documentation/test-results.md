# Test Results and Verification Report: Vehicle Rental System (RentRide)

This document records the empirical testing and verification performed against the live **Vehicle Rental System (RentRide)** running on **Apache Tomcat 9.0.120** with **MySQL 8.0** at `http://localhost:8084/RentalVehicleSystem/`.

---

## 1. Test Execution Summary

- **Total Test Cases Executed:** 15
- **Passed:** 15
- **Failed:** 0
- **Not Tested:** 0
- **Success Rate:** 100.0%
- **Execution Date:** October 26, 2026
- **Test Mode:** Automated Integration & Functional Browser Verification (Headless Edge / Selenium & Python HTTP Test Harness)

---

## 2. Detailed Test Results Table

| Test ID | Feature Tested | Steps / Request Performed | Expected Result | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Landing Page Rendering | Send `GET /RentalVehicleSystem/` as unauthenticated guest. | HTTP 200 OK; page displays "RentRide" title, Hero banner, and guest navbar ("Home", "Browse Vehicles", "Login", "Register"). | HTTP 200 OK returned; complete HTML structure and navbar links verified. | **PASS** |
| **TC-02** | Static Vehicle Imagery Serving | Send `GET /images/vehicles/{swift, creta, city, fortuner, hunter, default}.jpg`. | HTTP 200 OK with `image/jpeg` MIME type and non-zero byte size (>10KB). | All 6 vehicle images served with valid `image/jpeg` content headers (ranging from 616KB to 905KB). | **PASS** |
| **TC-03** | Public Vehicle Catalog | Send `GET /vehicles` without an active session. | HTTP 200 OK; catalog displays dynamic cards for all available vehicles with brand, model, daily price, and type badges. | HTTP 200 OK; cards rendered with vehicle photos, daily rates, and "Book Now" CTA buttons. | **PASS** |
| **TC-04** | Vehicle Details Inspection | Send `GET /vehicle-details?id=2` (Hyundai Creta). | HTTP 200 OK; page displays full vehicle attributes, registration number, daily rate, and booking button. | HTTP 200 OK; Hyundai Creta details, specifications, and booking link rendered accurately. | **PASS** |
| **TC-05** | Customer Account Registration | Send `POST /register` with valid name, unique timestamped email, and password. | HTTP 302 Redirect to `/login.jsp?registered=1`; password securely hashed using BCrypt in MySQL database. | Registration succeeded; database user inserted with hashed password; redirected with success banner. | **PASS** |
| **TC-06** | Customer Authentication & Session | Send `POST /login` with registered customer credentials. | Valid session created; session attributes `userId`, `userName`, `userRole` set; redirected to `/vehicles`. | Authenticated successfully; navbar updated with "My Bookings", customer name greeting, and "Logout". | **PASS** |
| **TC-07** | Booking Reservation Creation | Send `POST /booking` for Hyundai Creta with future pick-up and drop-off dates. | Booking record created in `bookings` table with status `PENDING`; user redirected to mock payment screen. | Booking #5 created with status `PENDING`; auto-redirected to `/payment?bookingId=5`. | **PASS** |
| **TC-08** | Mock Payment Sandbox Rendering | Send `GET /payment?bookingId=5` with active customer session. | HTTP 200 OK; payment screen displays mock simulation banner, reservation summary, total payable, and payment methods. | Mock payment sandbox rendered with test methods (Card, UPI, Netbanking) and pricing summary. | **PASS** |
| **TC-09** | Payment Authorization & Confirmation | Send `POST /payment` with `paymentStatus=SUCCESS` for Booking #5. | Payment inserted in `payments` table; booking status updated to `CONFIRMED`; redirected to `/my-bookings`. | Payment settled; booking marked `CONFIRMED`; displayed in customer dashboard with confirmed badge. | **PASS** |
| **TC-10** | Reservation Overlap Conflict Detection | Send `POST /booking` on same vehicle (Creta) for identical or overlapping dates. | Booking rejected; transaction rolled back; error banner: "Vehicle is unavailable or has an overlapping booking". | Conflict detected; overlap query blocked duplicate booking; returned user-friendly error message. | **PASS** |
| **TC-11** | Admin Authentication & RBAC | Send `POST /login` with administrator credentials (`admin@rental.com`). | Authenticated with `ADMIN` role; session initialized; redirected to `/admin/dashboard`. | Admin logged in; admin navbar rendered ("Admin Dashboard", "Manage Vehicles", "Manage Bookings", "Logout"). | **PASS** |
| **TC-12** | Admin Operational Dashboard | Send `GET /admin/dashboard` as authenticated Admin. | HTTP 200 OK; dashboard metrics loaded (Gross Revenue, Total Fleet, Active Bookings, Registered Users). | HTTP 200 OK; all operational KPIs and recent reservation tables rendered with live database values. | **PASS** |
| **TC-13** | Admin Fleet Inventory Controls | Send `GET /admin/vehicles` as authenticated Admin. | Fleet inventory table rendered with vehicle photos, registration numbers, daily rates, and status badges. | Complete fleet listed; status toggles and "+ Add New Vehicle" interactive modal form verified. | **PASS** |
| **TC-14** | Admin Customer Reservations Control | Send `GET /admin/bookings` as authenticated Admin. | HTTP 200 OK; all customer bookings displayed with customer names, vehicle models, total amounts, and statuses. | All reservation records rendered with operational status controls. | **PASS** |
| **TC-15** | User Session Termination (Logout) | Send `GET /logout` with active user/admin session. | Session invalidated; cookies cleared; user redirected to landing page or login screen. | Session terminated; navigation reverted to guest view; unauthenticated access confirmed. | **PASS** |

---

## 3. Verified System Behaviors

1. **Transactional Integrity:** Overlapping reservations on the same vehicle are strictly prevented at both the application logic level and database query level via `SELECT ... FOR UPDATE` row-locking.
2. **Password Cryptography:** User passwords are never stored in plaintext; BCrypt with adaptive salting is verified during registration and login.
3. **Role-Based Access Control (RBAC):** Admin routes (`/admin/*`) require the `ADMIN` session role and redirect unauthenticated or non-admin requests safely.
4. **Mock Payment Architecture:** The payment workflow simulates real-world payment gateway interaction without requiring external API dependencies or incurring live financial charges.

---

## 4. Known Environmental Limitations

- **Email Dispatching:** The current implementation uses direct database registration and login without external SMTP email verification services.
- **Payment Processing:** Financial transactions are handled by the built-in development sandbox payment processor rather than a live payment gateway (Razorpay / Stripe) to avoid external API dependencies and costs.
