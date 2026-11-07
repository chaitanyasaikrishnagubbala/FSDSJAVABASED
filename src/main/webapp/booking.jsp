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
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Book <%= vehicle.getBrand() %> <%= vehicle.getModel() %> | RentRide</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>

    <main class="main-content">
        <div class="booking-container">
            <div class="booking-card">
                <div class="booking-preview">
                    <img src="${pageContext.request.contextPath}/<%= vehicle.getImageUrl() %>" 
                         alt="<%= vehicle.getBrand() %>" 
                         class="booking-preview-img"
                         onerror="this.src='${pageContext.request.contextPath}/images/vehicles/default.jpg'">
                    <div>
                        <span class="vehicle-type-tag"><%= vehicle.getType() %></span>
                        <h2><%= vehicle.getBrand() %> <%= vehicle.getModel() %></h2>
                        <p class="subtitle" style="margin-top:2px;">Reg: <%= vehicle.getVehicleNumber() %></p>
                        <p style="font-weight:700; color:var(--primary); margin-top:4px;">
                            ₹<span id="ratePerDay"><%= String.format("%.2f", vehicle.getPricePerDay()) %></span> / day
                        </p>
                    </div>
                </div>

                <% if (request.getAttribute("error") != null) { %>
                    <div class="message error">
                        <%= request.getAttribute("error") %>
                    </div>
                <% } %>

                <form action="${pageContext.request.contextPath}/booking" method="post" id="bookingForm">
                    <input type="hidden" name="vehicleId" value="<%= vehicle.getId() %>">

                    <div class="form-row">
                        <div class="form-group">
                            <label for="startDate">Pick-up Date</label>
                            <input type="date" id="startDate" name="startDate" required>
                        </div>

                        <div class="form-group">
                            <label for="endDate">Drop-off Date</label>
                            <input type="date" id="endDate" name="endDate" required>
                        </div>
                    </div>

                    <div class="price-breakdown" id="priceBreakdown" style="display:none;">
                        <div class="breakdown-row">
                            <span>Rental Duration:</span>
                            <strong id="totalDaysText">0 days</strong>
                        </div>
                        <div class="breakdown-row total-row">
                            <span>Estimated Total Amount:</span>
                            <strong id="totalPriceText" style="color:var(--primary);">₹0.00</strong>
                        </div>
                    </div>

                    <div style="display: flex; gap: 12px; margin-top: 24px;">
                        <button type="submit" class="btn btn-primary" style="flex:1;">Proceed to Payment</button>
                        <a href="${pageContext.request.contextPath}/vehicle-details?id=<%= vehicle.getId() %>" class="btn btn-outline">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>

    <script>
        const ratePerDay = <%= vehicle.getPricePerDay() %>;
        const startInput = document.getElementById('startDate');
        const endInput = document.getElementById('endDate');
        const priceBreakdown = document.getElementById('priceBreakdown');
        const daysText = document.getElementById('totalDaysText');
        const priceText = document.getElementById('totalPriceText');

        const today = new Date().toISOString().split('T')[0];
        startInput.min = today;
        endInput.min = today;

        function updatePrice() {
            if (startInput.value && endInput.value) {
                const start = new Date(startInput.value);
                const end = new Date(endInput.value);
                const diffTime = end - start;
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

                if (diffDays > 0) {
                    const total = diffDays * ratePerDay;
                    priceBreakdown.style.display = 'block';
                    daysText.textContent = diffDays + (diffDays === 1 ? ' day' : ' days');
                    priceText.textContent = '₹' + total.toFixed(2);
                } else {
                    priceBreakdown.style.display = 'none';
                }
            }
        }

        startInput.addEventListener('change', () => {
            endInput.min = startInput.value;
            updatePrice();
        });
        endInput.addEventListener('change', updatePrice);
    </script>
</body>
</html>
