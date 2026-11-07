<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List,com.rental.model.Booking" %>
<%
    List<Booking> bookings = (List<Booking>) request.getAttribute("bookings");
    if (bookings == null) {
        response.sendRedirect(request.getContextPath() + "/admin/bookings");
        return;
    }
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Manage Bookings | RentRide Admin</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="../includes/navbar.jsp" %>

    <main class="main-content">
        <div class="content-container">
            <div class="page-header">
                <div>
                    <h1>Customer Reservations Control</h1>
                    <p class="subtitle">Review booking requests, manual status overrides, and booking history.</p>
                </div>
            </div>

            <div class="table-card">
                <% if (bookings.isEmpty()) { %>
                    <div style="text-align: center; padding: 40px; color: var(--text-muted);">
                        No customer reservations recorded yet.
                    </div>
                <% } else { %>
                    <div class="responsive-table-wrapper">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Ref ID</th>
                                    <th>Customer Details</th>
                                    <th>Reserved Vehicle</th>
                                    <th>Rental Window</th>
                                    <th>Total (₹)</th>
                                    <th>Status</th>
                                    <th>Staff Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <% for (Booking b : bookings) { %>
                                    <tr>
                                        <td><strong>#<%= b.getId() %></strong></td>
                                        <td>
                                            <strong style="color:var(--dark);"><%= b.getUserName() != null ? b.getUserName() : "User #" + b.getUserId() %></strong><br>
                                            <small style="color:var(--text-muted);"><%= b.getUserEmail() != null ? b.getUserEmail() : "" %></small>
                                        </td>
                                        <td>
                                            <strong><%= b.getVehicleName() != null ? b.getVehicleName() : "Vehicle #" + b.getVehicleId() %></strong>
                                            <% if (b.getVehicleNumber() != null) { %>
                                                <br><small style="color:var(--text-muted); font-size:12px;"><%= b.getVehicleNumber() %></small>
                                            <% } %>
                                        </td>
                                        <td>
                                            <span><%= b.getStartDate() %></span><br>
                                            <small style="color:var(--text-muted);">&darr; to</small><br>
                                            <span><%= b.getEndDate() %></span>
                                        </td>
                                        <td><strong style="color:var(--dark);">₹<%= String.format("%.2f", b.getTotalAmount()) %></strong></td>
                                        <td>
                                            <span class="status-badge status-<%= b.getStatus().toLowerCase() %>">
                                                <%= b.getStatus() %>
                                            </span>
                                        </td>
                                        <td class="action-cell">
                                            <% if ("PENDING".equalsIgnoreCase(b.getStatus())) { %>
                                                <form action="${pageContext.request.contextPath}/admin/bookings" method="post" style="display:inline;">
                                                    <input type="hidden" name="bookingId" value="<%= b.getId() %>">
                                                    <input type="hidden" name="status" value="CONFIRMED">
                                                    <button type="submit" class="btn-sm btn-action-pay">Approve</button>
                                                </form>

                                                <form action="${pageContext.request.contextPath}/admin/bookings" method="post" style="display:inline;">
                                                    <input type="hidden" name="bookingId" value="<%= b.getId() %>">
                                                    <input type="hidden" name="status" value="REJECTED">
                                                    <button type="submit" class="btn-sm btn-action-delete">Reject</button>
                                                </form>
                                            <% } else if ("CONFIRMED".equalsIgnoreCase(b.getStatus())) { %>
                                                <form action="${pageContext.request.contextPath}/admin/bookings" method="post" style="display:inline;">
                                                    <input type="hidden" name="bookingId" value="<%= b.getId() %>">
                                                    <input type="hidden" name="status" value="CANCELLED">
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
