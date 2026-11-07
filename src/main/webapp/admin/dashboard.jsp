<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List,com.rental.model.Booking" %>
<%
    Integer totalVehicles = (Integer) request.getAttribute("totalVehicles");
    if (totalVehicles == null) {
        response.sendRedirect(request.getContextPath() + "/admin/dashboard");
        return;
    }
    Integer availableVehicles = (Integer) request.getAttribute("availableVehicles");
    Integer totalBookings = (Integer) request.getAttribute("totalBookings");
    Integer pendingBookings = (Integer) request.getAttribute("pendingBookings");
    Double totalRevenue = (Double) request.getAttribute("totalRevenue");
    List<Booking> recentBookings = (List<Booking>) request.getAttribute("recentBookings");
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Admin Dashboard | RentRide</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="../includes/navbar.jsp" %>

    <main class="main-content">
        <div class="content-container">
            <div class="page-header">
                <div>
                    <h1>Operational Dashboard</h1>
                    <p class="subtitle">Real-time fleet metrics, revenue performance, and pending requests.</p>
                </div>
                <div>
                    <a href="${pageContext.request.contextPath}/admin/vehicles" class="btn btn-primary">+ Add Vehicle</a>
                </div>
            </div>

            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-title">Total Fleet Units</span>
                    <span class="metric-value"><%= totalVehicles %></span>
                    <span class="metric-sub"><%= availableVehicles %> Available for rent</span>
                </div>
                <div class="metric-card">
                    <span class="metric-title">Active / Ready Fleet</span>
                    <span class="metric-value text-success"><%= availableVehicles %></span>
                    <span class="metric-sub">Immediate dispatch ready</span>
                </div>
                <div class="metric-card">
                    <span class="metric-title">Total Bookings</span>
                    <span class="metric-value"><%= totalBookings %></span>
                    <span class="metric-sub"><%= pendingBookings %> Awaiting approval</span>
                </div>
                <div class="metric-card">
                    <span class="metric-title">Pending Approvals</span>
                    <span class="metric-value text-warning"><%= pendingBookings %></span>
                    <span class="metric-sub">Requires staff review</span>
                </div>
                <div class="metric-card">
                    <span class="metric-title">Gross Revenue</span>
                    <span class="metric-value text-primary">₹<%= String.format("%.2f", totalRevenue != null ? totalRevenue : 0.0) %></span>
                    <span class="metric-sub">Settled transactions</span>
                </div>
            </div>

            <div style="margin-top: 36px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 16px;">
                    <h2 style="font-size: 20px; font-weight: 700; color: var(--dark);">Recent Reservations</h2>
                    <a href="${pageContext.request.contextPath}/admin/bookings" style="font-size: 13px; font-weight: 600;">View All Bookings &rarr;</a>
                </div>

                <div class="table-card">
                    <% if (recentBookings == null || recentBookings.isEmpty()) { %>
                        <div style="text-align: center; padding: 40px; color: var(--text-muted);">
                            No reservations recorded yet.
                        </div>
                    <% } else { %>
                        <div class="responsive-table-wrapper">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Ref ID</th>
                                        <th>Customer</th>
                                        <th>Vehicle</th>
                                        <th>Dates</th>
                                        <th>Total (₹)</th>
                                        <th>Status</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <% for (Booking b : recentBookings) { %>
                                        <tr>
                                            <td><strong>#<%= b.getId() %></strong></td>
                                            <td>
                                                <strong><%= b.getUserName() != null ? b.getUserName() : "User #" + b.getUserId() %></strong><br>
                                                <small style="color:var(--text-muted);"><%= b.getUserEmail() != null ? b.getUserEmail() : "" %></small>
                                            </td>
                                            <td><%= b.getVehicleName() != null ? b.getVehicleName() : "Vehicle #" + b.getVehicleId() %></td>
                                            <td><%= b.getStartDate() %> &rarr; <%= b.getEndDate() %></td>
                                            <td><strong>₹<%= String.format("%.2f", b.getTotalAmount()) %></strong></td>
                                            <td>
                                                <span class="status-badge status-<%= b.getStatus().toLowerCase() %>">
                                                    <%= b.getStatus() %>
                                                </span>
                                            </td>
                                            <td>
                                                <a href="${pageContext.request.contextPath}/admin/bookings" class="btn-sm">Manage</a>
                                            </td>
                                        </tr>
                                    <% } %>
                                </tbody>
                            </table>
                        </div>
                    <% } %>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>
</body>
</html>
