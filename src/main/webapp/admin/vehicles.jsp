<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List,com.rental.model.Vehicle" %>
<%
    List<Vehicle> vehicles = (List<Vehicle>) request.getAttribute("vehicles");
    if (vehicles == null) {
        response.sendRedirect(request.getContextPath() + "/admin/vehicles");
        return;
    }
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Manage Fleet | RentRide Admin</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <%@ include file="../includes/navbar.jsp" %>

    <main class="main-content">
        <div class="content-container">
            <div class="page-header">
                <div>
                    <h1>Fleet Inventory Management</h1>
                    <p class="subtitle">Add new rental units, adjust daily rates, and control availability.</p>
                </div>
                <button type="button" class="btn btn-primary" onclick="toggleAddForm()">+ Add New Vehicle</button>
            </div>

            <!-- Add Vehicle Form Card -->
            <div class="table-card" id="addVehicleForm" style="display:none; padding: 28px; margin-bottom: 28px;">
                <h3 style="margin-bottom: 18px; color: var(--dark);">Add New Vehicle to Fleet</h3>
                <form action="${pageContext.request.contextPath}/admin/vehicles" method="post">
                    <input type="hidden" name="action" value="add">

                    <div class="form-row">
                        <div class="form-group">
                            <label for="vehicleNumber">Registration Number</label>
                            <input type="text" id="vehicleNumber" name="vehicleNumber" placeholder="e.g. AP39XY9999" required>
                        </div>
                        <div class="form-group">
                            <label for="brand">Brand / Make</label>
                            <input type="text" id="brand" name="brand" placeholder="e.g. Maruti / Hyundai" required>
                        </div>
                        <div class="form-group">
                            <label for="model">Model Name</label>
                            <input type="text" id="model" name="model" placeholder="e.g. Swift / Creta" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="type">Vehicle Class</label>
                            <select id="type" name="type" required class="form-select">
                                <option value="Hatchback">Hatchback</option>
                                <option value="Sedan" selected>Sedan</option>
                                <option value="SUV">SUV</option>
                                <option value="Luxury">Luxury</option>
                                <option value="Bike">Motorcycle / Scooter</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="pricePerDay">Daily Rate (₹)</label>
                            <input type="number" id="pricePerDay" name="pricePerDay" step="0.01" min="1" placeholder="e.g. 1800.00" required>
                        </div>
                    </div>

                    <div style="display:flex; gap:12px; margin-top:16px;">
                        <button type="submit" class="btn btn-success">Save to Fleet</button>
                        <button type="button" class="btn btn-secondary" onclick="toggleAddForm()">Cancel</button>
                    </div>
                </form>
            </div>

            <!-- Vehicles Table -->
            <div class="table-card">
                <div class="responsive-table-wrapper">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Photo</th>
                                <th>Vehicle</th>
                                <th>Registration</th>
                                <th>Category</th>
                                <th>Rate / Day</th>
                                <th>Availability Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <% for (Vehicle v : vehicles) { %>
                                <tr>
                                    <td>
                                        <img src="${pageContext.request.contextPath}/<%= v.getImageUrl() %>" 
                                             alt="<%= v.getBrand() %>" 
                                             style="width: 72px; height: 46px; object-fit: cover; border-radius: 6px; border: 1px solid var(--border);"
                                             onerror="this.src='${pageContext.request.contextPath}/images/vehicles/default.jpg'">
                                    </td>
                                    <td>
                                        <strong><%= v.getBrand() %> <%= v.getModel() %></strong>
                                    </td>
                                    <td><code><%= v.getVehicleNumber() %></code></td>
                                    <td><%= v.getType() %></td>
                                    <td><strong>₹<%= String.format("%.2f", v.getPricePerDay()) %></strong></td>
                                    <td>
                                        <form action="${pageContext.request.contextPath}/admin/vehicles" method="post" style="display:inline;">
                                            <input type="hidden" name="action" value="toggleStatus">
                                            <input type="hidden" name="id" value="<%= v.getId() %>">
                                            <button type="submit" class="status-toggle-btn <%= "AVAILABLE".equalsIgnoreCase(v.getStatus()) ? "status-available" : "status-unavailable" %>" title="Click to toggle status">
                                                <%= v.getStatus() %>
                                            </button>
                                        </form>
                                    </td>
                                    <td class="action-cell">
                                        <button type="button" class="btn-sm btn-action-edit"
                                                onclick="openEditModal(<%= v.getId() %>, '<%= v.getVehicleNumber() %>', '<%= v.getBrand() %>', '<%= v.getModel() %>', '<%= v.getType() %>', <%= v.getPricePerDay() %>, '<%= v.getStatus() %>')">
                                            Edit
                                        </button>

                                        <form action="${pageContext.request.contextPath}/admin/vehicles" method="post" style="display:inline;" onsubmit="return confirm('Delete vehicle <%= v.getBrand() %> <%= v.getModel() %>?');">
                                            <input type="hidden" name="action" value="delete">
                                            <input type="hidden" name="id" value="<%= v.getId() %>">
                                            <button type="submit" class="btn-sm btn-action-delete">Delete</button>
                                        </form>
                                    </td>
                                </tr>
                            <% } %>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </main>

    <!-- Edit Vehicle Modal -->
    <div id="editModal" class="modal-overlay" style="display:none;">
        <div class="modal-card">
            <h3 style="margin-bottom: 18px; color: var(--dark);">Edit Vehicle Details</h3>
            <form action="${pageContext.request.contextPath}/admin/vehicles" method="post">
                <input type="hidden" name="action" value="update">
                <input type="hidden" name="id" id="editId">

                <div class="form-group">
                    <label for="editNumber">Registration Number</label>
                    <input type="text" id="editNumber" name="vehicleNumber" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="editBrand">Brand</label>
                        <input type="text" id="editBrand" name="brand" required>
                    </div>
                    <div class="form-group">
                        <label for="editModel">Model</label>
                        <input type="text" id="editModel" name="model" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="editType">Category</label>
                        <input type="text" id="editType" name="type" required>
                    </div>
                    <div class="form-group">
                        <label for="editPrice">Daily Rate (₹)</label>
                        <input type="number" id="editPrice" name="pricePerDay" step="0.01" required>
                    </div>
                </div>
                <div class="form-group">
                    <label for="editStatus">Status</label>
                    <select id="editStatus" name="status" class="form-select">
                        <option value="AVAILABLE">AVAILABLE</option>
                        <option value="UNAVAILABLE">UNAVAILABLE</option>
                    </select>
                </div>

                <div class="modal-actions">
                    <button type="submit" class="btn btn-primary" style="flex:1;">Update Vehicle</button>
                    <button type="button" class="btn btn-secondary" onclick="closeEditModal()">Cancel</button>
                </div>
            </form>
        </div>
    </div>

    <footer class="footer">
        <p>&copy; 2026 RentRide Inc. Developed with Java Servlets, JSP, JDBC, MySQL & Tomcat 9.</p>
    </footer>

    <script>
        function toggleAddForm() {
            const form = document.getElementById('addVehicleForm');
            form.style.display = (form.style.display === 'none') ? 'block' : 'none';
        }

        function openEditModal(id, number, brand, model, type, price, status) {
            document.getElementById('editId').value = id;
            document.getElementById('editNumber').value = number;
            document.getElementById('editBrand').value = brand;
            document.getElementById('editModel').value = model;
            document.getElementById('editType').value = type;
            document.getElementById('editPrice').value = price;
            document.getElementById('editStatus').value = status;
            document.getElementById('editModal').style.display = 'flex';
        }

        function closeEditModal() {
            document.getElementById('editModal').style.display = 'none';
        }
    </script>
</body>
</html>
