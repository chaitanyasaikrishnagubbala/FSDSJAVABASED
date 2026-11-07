<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="com.rental.model.Vehicle" %>
<%
    Vehicle vehicle = (Vehicle) request.getAttribute("vehicle");
    if (vehicle == null) {
        response.sendRedirect(request.getContextPath() + "/vehicles");
        return;
    }
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title><%= vehicle.getBrand() %> <%= vehicle.getModel() %> | RentRide</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>

    <main class="main-content">
        <div class="details-container">
            <div class="details-card">
                <div class="details-image-wrapper">
                    <img src="${pageContext.request.contextPath}/<%= vehicle.getImageUrl() %>" 
                         alt="<%= vehicle.getBrand() %> <%= vehicle.getModel() %>" 
                         onerror="this.src='${pageContext.request.contextPath}/images/vehicles/default.jpg'">
                </div>

                <div class="details-info">
                    <span class="vehicle-type-tag"><%= vehicle.getType() %></span>
                    <h1><%= vehicle.getBrand() %> <%= vehicle.getModel() %></h1>
                    <p class="vehicle-meta">Registration: <strong><%= vehicle.getVehicleNumber() %></strong></p>
                    <p class="vehicle-meta">Status: 
                        <span class="status-badge <%= "AVAILABLE".equalsIgnoreCase(vehicle.getStatus()) ? "status-confirmed" : "status-cancelled" %>">
                            <%= vehicle.getStatus() %>
                        </span>
                    </p>

                    <div class="vehicle-price">
                        ₹<%= String.format("%.2f", vehicle.getPricePerDay()) %>
                        <span>/ day</span>
                    </div>

                    <div style="margin-top: 15px; margin-bottom: 25px;">
                        <% if ("AVAILABLE".equalsIgnoreCase(vehicle.getStatus())) { %>
                            <a class="btn btn-primary" style="width: 100%;"
                               href="${pageContext.request.contextPath}/booking?vehicleId=<%= vehicle.getId() %>">
                                Proceed to Booking
                            </a>
                        <% } else { %>
                            <div class="message error">This vehicle is currently unavailable for booking.</div>
                        <% } %>
                    </div>

                    <p>
                        <a href="${pageContext.request.contextPath}/vehicles" class="btn btn-outline" style="width: 100%;">
                            &larr; Back to Vehicle Catalog
                        </a>
                    </p>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>
</body>
</html>
