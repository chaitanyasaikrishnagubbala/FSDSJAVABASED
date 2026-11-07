<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Login | RentRide</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>

    <main class="main-content auth-wrapper">
        <div class="auth-container">
            <h2>Welcome Back</h2>
            <p class="subtitle">Log in to your RentRide account.</p>

            <% if (request.getAttribute("error") != null) { %>
                <div class="message error">
                    <%= request.getAttribute("error") %>
                </div>
            <% } %>

            <% if ("1".equals(request.getParameter("registered"))) { %>
                <div class="message success">
                    Registration successful! Please sign in with your credentials.
                </div>
            <% } %>

            <% if ("1".equals(request.getParameter("logout"))) { %>
                <div class="message info">
                    You have been logged out successfully.
                </div>
            <% } %>

            <form action="${pageContext.request.contextPath}/login" method="post">
                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" name="email" placeholder="name@example.com" required autocomplete="email">
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="••••••••" required autocomplete="current-password">
                </div>

                <button type="submit" class="btn btn-primary" style="width:100%; margin-top:10px;">Sign In</button>
            </form>

            <p class="auth-footer">
                Don't have an account?
                <a href="${pageContext.request.contextPath}/register.jsp"><strong>Register here</strong></a>
            </p>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>
</body>
</html>
