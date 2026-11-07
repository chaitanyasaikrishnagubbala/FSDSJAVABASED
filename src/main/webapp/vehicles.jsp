<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List,com.rental.model.Vehicle" %>
<%
    List<Vehicle> vehicles = (List<Vehicle>) request.getAttribute("vehicles");
    if (vehicles == null) {
        response.sendRedirect(request.getContextPath() + "/vehicles");
        return;
    }
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Browse Vehicles | RentRide</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>

    <main class="main-content">
        <div class="vehicles-main">
            <h1>Find Your Ideal Vehicle</h1>
            <p class="subtitle">Explore our maintained fleet ready for immediate booking.</p>

            <div class="vehicle-grid">
                <%
                    if (vehicles != null && !vehicles.isEmpty()) {
                        for (Vehicle v : vehicles) {
                %>
                    <article class="vehicle-card">
                        <div class="vehicle-image-wrapper">
                            <img src="${pageContext.request.contextPath}/<%= v.getImageUrl() %>" 
                                 alt="<%= v.getBrand() %> <%= v.getModel() %>" 
                                 class="vehicle-photo"
                                 loading="lazy"
                                 onerror="this.src='${pageContext.request.contextPath}/images/vehicles/default.jpg'">
                        </div>

                        <div class="vehicle-info">
                            <span class="vehicle-type-tag"><%= v.getType() %></span>
                            <h2><%= v.getBrand() %> <%= v.getModel() %></h2>
                            <p class="vehicle-number">Reg: <%= v.getVehicleNumber() %></p>
                            
                            <p class="vehicle-price">
                                ₹<%= String.format("%.2f", v.getPricePerDay()) %>
                                <span>/ day</span>
                            </p>

                            <a class="btn btn-primary"
                               href="${pageContext.request.contextPath}/vehicle-details?id=<%= v.getId() %>">
                                View Details & Book
                            </a>
                        </div>
                    </article>
                <%
                        }
                    } else {
                %>
                    <div class="empty-state" style="grid-column: 1/-1; text-align: center; padding: 60px 20px; background: white; border-radius: 12px; border: 1px solid var(--border);">
                        <div style="font-size: 48px; margin-bottom: 12px;">🚗</div>
                        <h2>No Vehicles Currently Available</h2>
                        <p class="subtitle">All vehicles are currently booked. Please check back shortly.</p>
                    </div>
                <%
                    }
                %>
            </div>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>
</body>
</html>
