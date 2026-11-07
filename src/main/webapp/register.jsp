<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Create Account | RentRide</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="includes/navbar.jsp" %>

    <main class="main-content auth-wrapper">
        <div class="auth-container">
            <h2>Create Account</h2>
            <p class="subtitle">Join RentRide to reserve cars and motorcycles.</p>

            <% if (request.getAttribute("error") != null) { %>
                <div class="message error">
                    <%= request.getAttribute("error") %>
                </div>
            <% } %>

            <form action="${pageContext.request.contextPath}/register" method="post">
                <div class="form-group">
                    <label for="name">Full Name</label>
                    <input type="text" id="name" name="name"
                           placeholder="Enter your full name"
                           maxlength="100" autocomplete="name" required>
                </div>

                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" name="email"
                           placeholder="name@example.com"
                           maxlength="100" autocomplete="email" required>
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password"
                           placeholder="Minimum 8 characters"
                           minlength="8" autocomplete="new-password" required>
                </div>

                <button type="submit" class="btn btn-primary" style="width:100%; margin-top:10px;">Create Account</button>
            </form>

            <p class="auth-footer">
                Already have an account?
                <a href="${pageContext.request.contextPath}/login.jsp"><strong>Sign in here</strong></a>
            </p>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>
</body>
</html>
