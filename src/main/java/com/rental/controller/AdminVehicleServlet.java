package com.rental.controller;

import com.rental.dao.VehicleDAO;
import com.rental.model.Vehicle;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.List;

@WebServlet("/admin/vehicles")
public class AdminVehicleServlet extends HttpServlet {

    private final VehicleDAO vehicleDAO = new VehicleDAO();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || !"ADMIN".equalsIgnoreCase((String) session.getAttribute("userRole"))) {
            response.sendRedirect(request.getContextPath() + "/login.jsp");
            return;
        }

        List<Vehicle> vehicles = vehicleDAO.getAllVehicles();
        request.setAttribute("vehicles", vehicles);
        request.getRequestDispatcher("/admin/vehicles.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        request.setCharacterEncoding("UTF-8");
        HttpSession session = request.getSession(false);
        if (session == null || !"ADMIN".equalsIgnoreCase((String) session.getAttribute("userRole"))) {
            response.sendRedirect(request.getContextPath() + "/login.jsp");
            return;
        }

        String action = request.getParameter("action");
        if (action == null) action = "";

        switch (action) {
            case "add": {
                String vehicleNumber = request.getParameter("vehicleNumber");
                String brand = request.getParameter("brand");
                String model = request.getParameter("model");
                String type = request.getParameter("type");
                String priceStr = request.getParameter("pricePerDay");

                if (vehicleNumber != null && brand != null && model != null && type != null && priceStr != null) {
                    try {
                        double pricePerDay = Double.parseDouble(priceStr.trim());
                        Vehicle vehicle = new Vehicle();
                        vehicle.setVehicleNumber(vehicleNumber.trim());
                        vehicle.setBrand(brand.trim());
                        vehicle.setModel(model.trim());
                        vehicle.setType(type.trim());
                        vehicle.setPricePerDay(pricePerDay);
                        vehicle.setStatus("AVAILABLE");

                        vehicleDAO.addVehicle(vehicle);
                    } catch (NumberFormatException ignored) {
                    }
                }
                break;
            }

            case "update": {
                String idStr = request.getParameter("id");
                String vehicleNumber = request.getParameter("vehicleNumber");
                String brand = request.getParameter("brand");
                String model = request.getParameter("model");
                String type = request.getParameter("type");
                String priceStr = request.getParameter("pricePerDay");
                String status = request.getParameter("status");

                if (idStr != null && vehicleNumber != null && brand != null && model != null && priceStr != null) {
                    try {
                        int id = Integer.parseInt(idStr.trim());
                        double pricePerDay = Double.parseDouble(priceStr.trim());
                        Vehicle vehicle = new Vehicle();
                        vehicle.setId(id);
                        vehicle.setVehicleNumber(vehicleNumber.trim());
                        vehicle.setBrand(brand.trim());
                        vehicle.setModel(model.trim());
                        vehicle.setType(type != null ? type.trim() : "Sedan");
                        vehicle.setPricePerDay(pricePerDay);
                        vehicle.setStatus(status != null ? status.trim() : "AVAILABLE");

                        vehicleDAO.updateVehicle(vehicle);
                    } catch (NumberFormatException ignored) {
                    }
                }
                break;
            }

            case "delete": {
                String idStr = request.getParameter("id");
                if (idStr != null) {
                    try {
                        int id = Integer.parseInt(idStr.trim());
                        vehicleDAO.deleteVehicle(id);
                    } catch (NumberFormatException ignored) {
                    }
                }
                break;
            }

            case "toggleStatus": {
                String idStr = request.getParameter("id");
                if (idStr != null) {
                    try {
                        int id = Integer.parseInt(idStr.trim());
                        Vehicle vehicle = vehicleDAO.getVehicleById(id);
                        if (vehicle != null) {
                            String newStatus = "AVAILABLE".equalsIgnoreCase(vehicle.getStatus()) ? "UNAVAILABLE" : "AVAILABLE";
                            vehicle.setStatus(newStatus);
                            vehicleDAO.updateVehicle(vehicle);
                        }
                    } catch (NumberFormatException ignored) {
                    }
                }
                break;
            }
        }

        response.sendRedirect(request.getContextPath() + "/admin/vehicles");
    }
}
