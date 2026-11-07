<%@ page pageEncoding="UTF-8" %>
<%
    String navUserRole = (String) session.getAttribute("userRole");
    String navUserName = (String) session.getAttribute("userName");
    Integer navUserId = (Integer) session.getAttribute("userId");
    boolean navIsLoggedIn = (navUserId != null);
    boolean navIsAdmin = "ADMIN".equalsIgnoreCase(navUserRole);
%>
<header class="site-header">
    <div class="header-container">
        <a class="nav-brand" href="${pageContext.request.contextPath}/index.jsp">
            <span class="brand-logo-icon">🚗</span>
            <span class="brand-text">RentRide</span>
        </a>

        <nav class="nav-menu">
            <% if (!navIsLoggedIn) { %>
                <a href="${pageContext.request.contextPath}/index.jsp" class="nav-link">Home</a>
                <a href="${pageContext.request.contextPath}/vehicles" class="nav-link">Browse Vehicles</a>
                <a href="${pageContext.request.contextPath}/login.jsp" class="nav-link">Login</a>
                <a href="${pageContext.request.contextPath}/register.jsp" class="btn btn-primary btn-nav">Register</a>
            <% } else if (navIsAdmin) { %>
                <a href="${pageContext.request.contextPath}/index.jsp" class="nav-link">Home</a>
                <a href="${pageContext.request.contextPath}/admin/dashboard" class="nav-link">Admin Dashboard</a>
                <a href="${pageContext.request.contextPath}/admin/vehicles" class="nav-link">Manage Vehicles</a>
                <a href="${pageContext.request.contextPath}/admin/bookings" class="nav-link">Manage Bookings</a>
                <div class="user-pill admin-pill">
                    <span class="role-badge">Admin</span>
                    <span class="user-name"><%= navUserName != null ? navUserName : "Admin" %></span>
                </div>
                <a href="${pageContext.request.contextPath}/logout" class="btn btn-outline btn-nav">Logout</a>
            <% } else { %>
                <a href="${pageContext.request.contextPath}/index.jsp" class="nav-link">Home</a>
                <a href="${pageContext.request.contextPath}/vehicles" class="nav-link">Browse Vehicles</a>
                <a href="${pageContext.request.contextPath}/my-bookings" class="nav-link">My Bookings</a>
                <div class="user-pill">
                    <span class="user-icon">👤</span>
                    <span class="user-name"><%= navUserName != null ? navUserName : "User" %></span>
                </div>
                <a href="${pageContext.request.contextPath}/logout" class="btn btn-outline btn-nav">Logout</a>
            <% } %>
        </nav>
    </div>
</header>
