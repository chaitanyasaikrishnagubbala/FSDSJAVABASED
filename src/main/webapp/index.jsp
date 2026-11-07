<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>RentRide — Modern Vehicle Rental Experience</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>

    <main class="main-content">
        <div class="landing-main">
            <section class="hero-section">
                <span class="badge">Drive Your Next Journey</span>
                <h1>Premium Vehicles,<br>Uncompromised Freedom.</h1>
                <p class="subtitle">Experience hassle-free car and motorcycle rentals at transparent daily rates with instant online reservation and verified fleet quality.</p>
                
                <div class="hero-actions">
                    <a href="${pageContext.request.contextPath}/vehicles" class="btn btn-primary">Browse Available Vehicles</a>
                    <% if (session.getAttribute("userId") == null) { %>
                        <a href="${pageContext.request.contextPath}/register.jsp" class="btn btn-secondary">Create Free Account</a>
                    <% } else { %>
                        <a href="${pageContext.request.contextPath}/my-bookings" class="btn btn-secondary">View My Bookings</a>
                    <% } %>
                </div>
            </section>

            <section class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Instant Online Booking</h3>
                    <p>Reserve vehicles in seconds with live availability and automatic overlap scheduling protection.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🛡️</div>
                    <h3>Verified & Inspected Fleet</h3>
                    <p>All cars and bikes are thoroughly cleaned, serviced, and insured before every single journey.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💳</div>
                    <h3>Transparent Pricing</h3>
                    <p>Clear daily pricing with zero hidden surcharges, fast mock sandbox payments, and instant confirmation.</p>
                </div>
            </section>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>
</body>
</html>
