<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List,com.rental.model.Booking" %>
<%
    List<Booking> bookings = (List<Booking>) request.getAttribute("bookings");
    if (bookings == null) {
        response.sendRedirect(request.getContextPath() + "/my-bookings");
        return;
    }
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My Bookings | RentRide</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>

    <main class="main-content">
        <div class="content-container">
            <div class="page-header">
                <div>
                    <h1>My Reservations</h1>
                    <p class="subtitle">Manage your current vehicle rentals, payment statuses, and history.</p>
                </div>
                <a href="${pageContext.request.contextPath}/vehicles" class="btn btn-primary">+ Rent Another Vehicle</a>
            </div>

            <% if ("success".equals(request.getParameter("payment"))) { %>
                <div class="message success">
                    <span>✓</span> Payment completed successfully! Your vehicle reservation is now confirmed.
                </div>
            <% } %>

            <% if ("cancelled".equals(request.getParameter("msg"))) { %>
                <div class="message success">
                    <span>✓</span> Reservation has been successfully cancelled.
                </div>
            <% } %>

            <% if ("already_confirmed".equals(request.getParameter("info"))) { %>
                <div class="message info">
                    <span>ℹ</span> This reservation is already confirmed and active.
                </div>
            <% } %>

            <% if (request.getParameter("error") != null) { %>
                <div class="message error">
                    <span>⚠</span> <%= request.getParameter("error") %>
                </div>
            <% } %>

            <div class="table-card">
                <% if (bookings.isEmpty()) { %>
                    <div style="text-align: center; padding: 60px 20px;">
                        <div style="font-size: 48px; margin-bottom: 12px;">🚗</div>
                        <h2>No Bookings Yet</h2>
                        <p class="subtitle" style="margin-bottom: 24px;">You haven't reserved any vehicles with us yet.</p>
                        <a href="${pageContext.request.contextPath}/vehicles" class="btn btn-primary">Find a Vehicle</a>
                    </div>
                <% } else { %>
                    <div class="responsive-table-wrapper">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Ref ID</th>
                                    <th>Vehicle</th>
                                    <th>Pick-up Date</th>
                                    <th>Drop-off Date</th>
                                    <th>Total Payable</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <% for (Booking b : bookings) { %>
                                    <tr>
                                        <td><strong>#<%= b.getId() %></strong></td>
                                        <td>
                                            <div style="font-weight: 700; color: var(--dark);">
                                                <%= b.getVehicleName() != null && !b.getVehicleName().isBlank() ? b.getVehicleName() : ("Vehicle #" + b.getVehicleId()) %>
                                            </div>
                                            <% if (b.getVehicleNumber() != null) { %>
                                                <div style="font-size: 12px; color: var(--text-muted);"><%= b.getVehicleNumber() %></div>
                                            <% } %>
                                        </td>
                                        <td><%= b.getStartDate() %></td>
                                        <td><%= b.getEndDate() %></td>
                                        <td><strong style="color:var(--dark);">₹<%= String.format("%.2f", b.getTotalAmount()) %></strong></td>
                                        <td>
                                            <span class="status-badge status-<%= b.getStatus().toLowerCase() %>">
                                                <%= b.getStatus() %>
                                            </span>
                                        </td>
                                        <td class="action-cell">
                                            <% if ("PENDING".equalsIgnoreCase(b.getStatus())) { %>
                                                <a href="${pageContext.request.contextPath}/payment?bookingId=<%= b.getId() %>" class="btn-sm btn-action-pay">Pay Now</a>
                                                <form action="${pageContext.request.contextPath}/cancel-booking" method="post" style="display:inline;" onsubmit="return confirm('Cancel this reservation?');">
                                                    <input type="hidden" name="bookingId" value="<%= b.getId() %>">
                                                    <button type="submit" class="btn-sm btn-action-cancel">Cancel</button>
                                                </form>
                                            <% } else if ("CONFIRMED".equalsIgnoreCase(b.getStatus())) { %>
                                                <form action="${pageContext.request.contextPath}/cancel-booking" method="post" style="display:inline;" onsubmit="return confirm('Cancel this confirmed reservation?');">
                                                    <input type="hidden" name="bookingId" value="<%= b.getId() %>">
                                                    <button type="submit" class="btn-sm btn-action-cancel">Cancel</button>
                                                </form>
                                            <% } else { %>
                                                <span style="color:var(--text-light); font-size:13px;">—</span>
                                            <% } %>
                                        </td>
                                    </tr>
                                <% } %>
                            </tbody>
                        </table>
                    </div>
                <% } %>
            </div>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>
</body>
</html>
