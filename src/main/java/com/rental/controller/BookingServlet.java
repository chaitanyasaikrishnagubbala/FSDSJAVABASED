package com.rental.controller;

import com.rental.dao.BookingDAO;
import com.rental.dao.VehicleDAO;
import com.rental.model.Booking;
import com.rental.model.Vehicle;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.sql.Date;
import java.time.LocalDate;

@WebServlet("/booking")
public class BookingServlet extends HttpServlet {

    private final BookingDAO bookingDAO = new BookingDAO();
    private final VehicleDAO vehicleDAO = new VehicleDAO();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("userId") == null) {
            response.sendRedirect(request.getContextPath() + "/login.jsp?error=" +
                    java.net.URLEncoder.encode("Please log in to book a vehicle.", "UTF-8"));
            return;
        }

        String vehicleIdStr = request.getParameter("vehicleId");
        if (vehicleIdStr == null || vehicleIdStr.isBlank()) {
            response.sendRedirect(request.getContextPath() + "/vehicles");
            return;
        }

        try {
            int vehicleId = Integer.parseInt(vehicleIdStr.trim());
            Vehicle vehicle = vehicleDAO.getVehicleById(vehicleId);

            if (vehicle == null) {
                response.sendError(HttpServletResponse.SC_NOT_FOUND, "Vehicle not found");
                return;
            }

            request.setAttribute("vehicle", vehicle);
            request.getRequestDispatcher("/booking.jsp").forward(request, response);

        } catch (NumberFormatException e) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "Invalid vehicle ID");
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        request.setCharacterEncoding("UTF-8");
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("userId") == null) {
            response.sendRedirect(request.getContextPath() + "/login.jsp");
            return;
        }

        int userId = (Integer) session.getAttribute("userId");
        String vehicleIdStr = request.getParameter("vehicleId");
        String startDateStr = request.getParameter("startDate");
        String endDateStr = request.getParameter("endDate");

        if (vehicleIdStr == null || startDateStr == null || endDateStr == null ||
            vehicleIdStr.isBlank() || startDateStr.isBlank() || endDateStr.isBlank()) {
            request.setAttribute("error", "All fields are required.");
            redispatchBookingForm(request, response, vehicleIdStr);
            return;
        }

        int vehicleId;
        Date startDate;
        Date endDate;

        try {
            vehicleId = Integer.parseInt(vehicleIdStr.trim());
            startDate = Date.valueOf(startDateStr.trim());
            endDate = Date.valueOf(endDateStr.trim());
        } catch (IllegalArgumentException e) {
            request.setAttribute("error", "Invalid date or vehicle selection format.");
            redispatchBookingForm(request, response, vehicleIdStr);
            return;
        }

        LocalDate today = LocalDate.now();
        if (startDate.toLocalDate().isBefore(today)) {
            request.setAttribute("error", "Start date cannot be in the past.");
            redispatchBookingForm(request, response, vehicleIdStr);
            return;
        }

        if (!endDate.after(startDate)) {
            request.setAttribute("error", "End date must be strictly after start date.");
            redispatchBookingForm(request, response, vehicleIdStr);
            return;
        }

        Booking booking = new Booking();
        booking.setUserId(userId);
        booking.setVehicleId(vehicleId);
        booking.setStartDate(startDate);
        booking.setEndDate(endDate);

        boolean created = bookingDAO.createBooking(booking);

        if (created) {
            // Forward to mock payment step
            response.sendRedirect(request.getContextPath() + "/payment?bookingId=" + booking.getId());
        } else {
            request.setAttribute("error", "Vehicle is unavailable or has an overlapping booking for the selected dates.");
            redispatchBookingForm(request, response, vehicleIdStr);
        }
    }

    private void redispatchBookingForm(HttpServletRequest request, HttpServletResponse response, String vehicleIdStr)
            throws ServletException, IOException {
        try {
            int vehicleId = Integer.parseInt(vehicleIdStr.trim());
            Vehicle vehicle = vehicleDAO.getVehicleById(vehicleId);
            request.setAttribute("vehicle", vehicle);
        } catch (Exception ignored) {
        }
        request.getRequestDispatcher("/booking.jsp").forward(request, response);
    }
}
