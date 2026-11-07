package com.rental.controller;

import com.rental.dao.BookingDAO;
import com.rental.dao.VehicleDAO;
import com.rental.model.Booking;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.List;

@WebServlet("/admin/dashboard")
public class AdminDashboardServlet extends HttpServlet {

    private final VehicleDAO vehicleDAO = new VehicleDAO();
    private final BookingDAO bookingDAO = new BookingDAO();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("userId") == null ||
            !"ADMIN".equalsIgnoreCase((String) session.getAttribute("userRole"))) {
            response.sendRedirect(request.getContextPath() + "/login.jsp?error=" +
                    java.net.URLEncoder.encode("Admin access required.", "UTF-8"));
            return;
        }

        int totalVehicles = vehicleDAO.countTotalVehicles();
        int availableVehicles = vehicleDAO.countAvailableVehicles();
        int totalBookings = bookingDAO.countTotalBookings();
        int pendingBookings = bookingDAO.countPendingBookings();
        double totalRevenue = bookingDAO.calculateTotalRevenue();

        List<Booking> allBookings = bookingDAO.getAllBookings();
        List<Booking> recentBookings = allBookings.size() > 5 ? allBookings.subList(0, 5) : allBookings;

        request.setAttribute("totalVehicles", totalVehicles);
        request.setAttribute("availableVehicles", availableVehicles);
        request.setAttribute("totalBookings", totalBookings);
        request.setAttribute("pendingBookings", pendingBookings);
        request.setAttribute("totalRevenue", totalRevenue);
        request.setAttribute("recentBookings", recentBookings);

        request.getRequestDispatcher("/admin/dashboard.jsp").forward(request, response);
    }
}
