<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="com.rental.model.Booking" %>
<%
    Booking booking = (Booking) request.getAttribute("booking");
    if (booking == null) {
        response.sendRedirect(request.getContextPath() + "/my-bookings");
        return;
    }
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mock Payment Sandbox | RentRide</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>

    <main class="main-content">
        <div class="payment-container">
            <div class="mock-banner">
                <span class="mock-badge">TEST SANDBOX</span>
                <p><strong>Development Payment Simulation</strong> — No actual currency or banking transactions occur.</p>
            </div>

            <% if (request.getParameter("error") != null) { %>
                <div class="message error">
                    <span>⚠</span> <%= request.getParameter("error") %>
                </div>
            <% } %>

            <div class="checkout-grid">
                <div class="checkout-summary-card">
                    <h2>Reservation Summary</h2>
                    <div class="summary-item">
                        <span style="color:var(--text-muted);">Booking Reference:</span>
                        <strong>#<%= booking.getId() %></strong>
                    </div>
                    <div class="summary-item">
                        <span style="color:var(--text-muted);">Vehicle:</span>
                        <strong><%= booking.getVehicleName() != null ? booking.getVehicleName() : ("Vehicle #" + booking.getVehicleId()) %></strong>
                    </div>
                    <div class="summary-item">
                        <span style="color:var(--text-muted);">Rental Window:</span>
                        <span><%= booking.getStartDate() %> &rarr; <%= booking.getEndDate() %></span>
                    </div>
                    <div class="summary-divider"></div>
                    <div class="summary-item" style="font-size: 17px; margin-top: 14px;">
                        <span>Total Payable:</span>
                        <strong class="highlight-price">₹<%= String.format("%.2f", booking.getTotalAmount()) %></strong>
                    </div>
                </div>

                <div class="checkout-actions-card">
                    <h2>Select Mock Payment Method</h2>

                    <form action="${pageContext.request.contextPath}/payment" method="post" id="paymentForm">
                        <input type="hidden" name="bookingId" value="<%= booking.getId() %>">
                        <input type="hidden" name="paymentStatus" id="paymentStatusInput" value="SUCCESS">

                        <div class="mock-methods">
                            <label class="method-option">
                                <input type="radio" name="mockMethod" value="CARD" checked>
                                <div>
                                    <strong style="display:block; font-size:14px;">💳 Simulated Credit/Debit Card</strong>
                                    <small style="color:var(--text-muted);">Mock instant card gateway</small>
                                </div>
                            </label>

                            <label class="method-option">
                                <input type="radio" name="mockMethod" value="UPI">
                                <div>
                                    <strong style="display:block; font-size:14px;">📱 Simulated UPI (Google Pay / PhonePe)</strong>
                                    <small style="color:var(--text-muted);">Mock instant UPI authorization</small>
                                </div>
                            </label>

                            <label class="method-option">
                                <input type="radio" name="mockMethod" value="NETBANKING">
                                <div>
                                    <strong style="display:block; font-size:14px;">🏦 Simulated Net Banking</strong>
                                    <small style="color:var(--text-muted);">Mock banking portal gateway</small>
                                </div>
                            </label>
                        </div>

                        <div class="payment-action-buttons">
                            <button type="submit" class="btn btn-success" onclick="document.getElementById('paymentStatusInput').value='SUCCESS';">
                                ✓ Authorize Successful Payment (₹<%= String.format("%.2f", booking.getTotalAmount()) %>)
                            </button>

                            <button type="submit" class="btn btn-danger-outline" onclick="document.getElementById('paymentStatusInput').value='FAILED';">
                                ✗ Simulate Payment Failure
                            </button>
                        </div>

                        <p style="text-align: center; margin-top: 20px;">
                            <a href="${pageContext.request.contextPath}/my-bookings" style="font-size: 13px; color: var(--text-muted);">
                                &larr; Return to My Bookings
                            </a>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>
</body>
</html>
