package com.rental.controller;

import com.rental.dao.BookingDAO;
import com.rental.dao.PaymentDAO;
import com.rental.model.Booking;
import com.rental.model.Payment;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

@WebServlet("/payment")
public class PaymentServlet extends HttpServlet {

    private final BookingDAO bookingDAO = new BookingDAO();
    private final PaymentDAO paymentDAO = new PaymentDAO();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("userId") == null) {
            response.sendRedirect(request.getContextPath() + "/login.jsp");
            return;
        }

        int userId = (Integer) session.getAttribute("userId");
        String role = (String) session.getAttribute("userRole");
        String bookingIdStr = request.getParameter("bookingId");

        if (bookingIdStr == null || bookingIdStr.isBlank()) {
            response.sendRedirect(request.getContextPath() + "/my-bookings");
            return;
        }

        try {
            int bookingId = Integer.parseInt(bookingIdStr.trim());
            Booking booking = bookingDAO.getBookingById(bookingId);

            if (booking == null) {
                response.sendError(HttpServletResponse.SC_NOT_FOUND, "Booking not found");
                return;
            }

            // Access control: only owner or admin can access payment
            if (booking.getUserId() != userId && !"ADMIN".equalsIgnoreCase(role)) {
                response.sendError(HttpServletResponse.SC_FORBIDDEN, "Access denied");
                return;
            }

            if ("CONFIRMED".equalsIgnoreCase(booking.getStatus())) {
                response.sendRedirect(request.getContextPath() + "/my-bookings?info=already_confirmed");
                return;
            }

            if ("CANCELLED".equalsIgnoreCase(booking.getStatus()) || "REJECTED".equalsIgnoreCase(booking.getStatus())) {
                response.sendRedirect(request.getContextPath() + "/my-bookings?error=invalid_status");
                return;
            }

            request.setAttribute("booking", booking);
            request.getRequestDispatcher("/payment.jsp").forward(request, response);

        } catch (NumberFormatException e) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "Invalid booking ID");
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
        String role = (String) session.getAttribute("userRole");
        String bookingIdStr = request.getParameter("bookingId");
        String actionStatus = request.getParameter("paymentStatus"); // "SUCCESS" or "FAILED"

        if (bookingIdStr == null || bookingIdStr.isBlank()) {
            response.sendRedirect(request.getContextPath() + "/my-bookings");
            return;
        }

        try {
            int bookingId = Integer.parseInt(bookingIdStr.trim());
            Booking booking = bookingDAO.getBookingById(bookingId);

            if (booking == null) {
                response.sendError(HttpServletResponse.SC_NOT_FOUND, "Booking not found");
                return;
            }

            if (booking.getUserId() != userId && !"ADMIN".equalsIgnoreCase(role)) {
                response.sendError(HttpServletResponse.SC_FORBIDDEN, "Access denied");
                return;
            }

            // Prevent duplicate payment if already confirmed
            if ("CONFIRMED".equalsIgnoreCase(booking.getStatus())) {
                response.sendRedirect(request.getContextPath() + "/my-bookings?info=already_confirmed");
                return;
            }

            String paymentStatus = ("FAILED".equalsIgnoreCase(actionStatus)) ? "FAILED" : "SUCCESS";

            Payment payment = new Payment();
            payment.setBookingId(bookingId);
            payment.setAmount(booking.getTotalAmount());
            payment.setPaymentStatus(paymentStatus);

            boolean processed = paymentDAO.processMockPayment(payment);

            if (processed && "SUCCESS".equals(paymentStatus)) {
                response.sendRedirect(request.getContextPath() + "/my-bookings?payment=success");
            } else if (processed && "FAILED".equals(paymentStatus)) {
                response.sendRedirect(request.getContextPath() + "/payment?bookingId=" + bookingId + "&error=Mock+payment+failed.+Please+retry.");
            } else {
                response.sendRedirect(request.getContextPath() + "/payment?bookingId=" + bookingId + "&error=Unable+to+process+payment.+Please+try+again.");
            }

        } catch (NumberFormatException e) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "Invalid booking ID");
        }
    }
}
