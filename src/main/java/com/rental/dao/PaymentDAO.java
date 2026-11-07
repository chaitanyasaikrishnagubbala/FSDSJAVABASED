package com.rental.dao;

import com.rental.model.Payment;
import com.rental.util.DBConnection;
import java.sql.*;

public class PaymentDAO {

    public boolean processMockPayment(Payment payment) {
        String bookingSql = "SELECT total_amount, status FROM bookings WHERE id=? FOR UPDATE";
        String insertSql = "INSERT INTO payments(booking_id, amount, payment_status) VALUES(?,?,?)";
        String confirmSql = "UPDATE bookings SET status='CONFIRMED' WHERE id=? AND status='PENDING'";

        String paymentStatus = payment.getPaymentStatus();

        if (!"SUCCESS".equals(paymentStatus) && !"FAILED".equals(paymentStatus)) {
            return false;
        }

        try (Connection con = DBConnection.getConnection()) {
            if (con == null) return false;
            con.setAutoCommit(false);

            try {
                double amount;

                try (PreparedStatement ps = con.prepareStatement(bookingSql)) {
                    ps.setInt(1, payment.getBookingId());

                    try (ResultSet rs = ps.executeQuery()) {
                        if (!rs.next() || !"PENDING".equals(rs.getString("status"))) {
                            con.rollback();
                            return false;
                        }
                        amount = rs.getDouble("total_amount");
                    }
                }

                try (PreparedStatement ps = con.prepareStatement(insertSql, Statement.RETURN_GENERATED_KEYS)) {
                    ps.setInt(1, payment.getBookingId());
                    ps.setDouble(2, amount);
                    ps.setString(3, paymentStatus);

                    if (ps.executeUpdate() == 0) {
                        con.rollback();
                        return false;
                    }

                    try (ResultSet keys = ps.getGeneratedKeys()) {
                        if (keys.next()) payment.setId(keys.getInt(1));
                    }
                }

                if ("SUCCESS".equals(paymentStatus)) {
                    try (PreparedStatement ps = con.prepareStatement(confirmSql)) {
                        ps.setInt(1, payment.getBookingId());

                        if (ps.executeUpdate() != 1) {
                            con.rollback();
                            return false;
                        }
                    }
                }

                payment.setAmount(amount);
                con.commit();
                return true;

            } catch (SQLException e) {
                con.rollback();
                throw e;
            } finally {
                con.setAutoCommit(true);
            }

        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public Payment getPaymentByBookingId(int bookingId) {
        String sql = "SELECT * FROM payments WHERE booking_id=? ORDER BY id DESC LIMIT 1";

        try (Connection con = DBConnection.getConnection()) {
            if (con == null) return null;

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, bookingId);

                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        Payment payment = new Payment();
                        payment.setId(rs.getInt("id"));
                        payment.setBookingId(rs.getInt("booking_id"));
                        payment.setAmount(rs.getDouble("amount"));
                        payment.setPaymentStatus(rs.getString("payment_status"));
                        payment.setPaymentDate(rs.getTimestamp("payment_date"));
                        return payment;
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }
}
