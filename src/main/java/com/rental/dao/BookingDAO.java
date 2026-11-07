package com.rental.dao;

import com.rental.model.Booking;
import com.rental.util.DBConnection;
import java.sql.*;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;

public class BookingDAO {

    public boolean createBooking(Booking booking) {
        if (booking.getStartDate() == null || booking.getEndDate() == null) return false;
        if (!booking.getEndDate().after(booking.getStartDate())) return false;

        String vehicleSql = "SELECT price_per_day, status FROM vehicles WHERE id=? FOR UPDATE";
        String overlapSql = "SELECT id FROM bookings WHERE vehicle_id=? AND status IN ('PENDING','CONFIRMED') AND start_date < ? AND end_date > ? LIMIT 1";
        String insertSql = "INSERT INTO bookings(user_id, vehicle_id, start_date, end_date, total_amount, status) VALUES(?,?,?,?,?,'PENDING')";

        try (Connection con = DBConnection.getConnection()) {
            if (con == null) return false;
            con.setAutoCommit(false);

            try {
                double pricePerDay;

                try (PreparedStatement ps = con.prepareStatement(vehicleSql)) {
                    ps.setInt(1, booking.getVehicleId());

                    try (ResultSet rs = ps.executeQuery()) {
                        if (!rs.next() || !"AVAILABLE".equalsIgnoreCase(rs.getString("status"))) {
                            con.rollback();
                            return false;
                        }
                        pricePerDay = rs.getDouble("price_per_day");
                    }
                }

                try (PreparedStatement ps = con.prepareStatement(overlapSql)) {
                    ps.setInt(1, booking.getVehicleId());
                    ps.setDate(2, booking.getEndDate());
                    ps.setDate(3, booking.getStartDate());

                    try (ResultSet rs = ps.executeQuery()) {
                        if (rs.next()) {
                            con.rollback();
                            return false;
                        }
                    }
                }

                long days = ChronoUnit.DAYS.between(
                    booking.getStartDate().toLocalDate(),
                    booking.getEndDate().toLocalDate()
                );
                if (days <= 0) days = 1;

                double totalAmount = days * pricePerDay;

                try (PreparedStatement ps = con.prepareStatement(insertSql, Statement.RETURN_GENERATED_KEYS)) {
                    ps.setInt(1, booking.getUserId());
                    ps.setInt(2, booking.getVehicleId());
                    ps.setDate(3, booking.getStartDate());
                    ps.setDate(4, booking.getEndDate());
                    ps.setDouble(5, totalAmount);

                    if (ps.executeUpdate() == 0) {
                        con.rollback();
                        return false;
                    }

                    try (ResultSet keys = ps.getGeneratedKeys()) {
                        if (keys.next()) booking.setId(keys.getInt(1));
                    }
                }

                booking.setTotalAmount(totalAmount);
                booking.setStatus("PENDING");
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

    public List<Booking> getBookingsByUser(int userId) {
        List<Booking> bookings = new ArrayList<>();
        String sql = "SELECT b.*, v.brand, v.model, v.vehicle_number " +
                     "FROM bookings b " +
                     "LEFT JOIN vehicles v ON b.vehicle_id = v.id " +
                     "WHERE b.user_id=? ORDER BY b.id DESC";

        try (Connection con = DBConnection.getConnection()) {
            if (con == null) return bookings;

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, userId);

                try (ResultSet rs = ps.executeQuery()) {
                    while (rs.next()) {
                        Booking b = mapBooking(rs);
                        String brand = rs.getString("brand");
                        String model = rs.getString("model");
                        b.setVehicleName((brand != null ? brand : "") + " " + (model != null ? model : ""));
                        b.setVehicleNumber(rs.getString("vehicle_number"));
                        bookings.add(b);
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return bookings;
    }

    public List<Booking> getAllBookings() {
        List<Booking> bookings = new ArrayList<>();
        String sql = "SELECT b.*, v.brand, v.model, v.vehicle_number, u.name AS user_name, u.email AS user_email " +
                     "FROM bookings b " +
                     "LEFT JOIN vehicles v ON b.vehicle_id = v.id " +
                     "LEFT JOIN users u ON b.user_id = u.id " +
                     "ORDER BY b.id DESC";

        try (Connection con = DBConnection.getConnection()) {
            if (con == null) return bookings;

            try (PreparedStatement ps = con.prepareStatement(sql);
                 ResultSet rs = ps.executeQuery()) {

                while (rs.next()) {
                    Booking b = mapBooking(rs);
                    String brand = rs.getString("brand");
                    String model = rs.getString("model");
                    b.setVehicleName((brand != null ? brand : "") + " " + (model != null ? model : ""));
                    b.setVehicleNumber(rs.getString("vehicle_number"));
                    b.setUserName(rs.getString("user_name"));
                    b.setUserEmail(rs.getString("user_email"));
                    bookings.add(b);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return bookings;
    }

    public Booking getBookingById(int id) {
        String sql = "SELECT b.*, v.brand, v.model, v.vehicle_number, u.name AS user_name, u.email AS user_email " +
                     "FROM bookings b " +
                     "LEFT JOIN vehicles v ON b.vehicle_id = v.id " +
                     "LEFT JOIN users u ON b.user_id = u.id " +
                     "WHERE b.id=?";

        try (Connection con = DBConnection.getConnection()) {
            if (con == null) return null;

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, id);

                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        Booking b = mapBooking(rs);
                        String brand = rs.getString("brand");
                        String model = rs.getString("model");
                        b.setVehicleName((brand != null ? brand : "") + " " + (model != null ? model : ""));
                        b.setVehicleNumber(rs.getString("vehicle_number"));
                        b.setUserName(rs.getString("user_name"));
                        b.setUserEmail(rs.getString("user_email"));
                        return b;
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public boolean cancelBooking(int bookingId, int userId) {
        String sql = "UPDATE bookings SET status='CANCELLED' WHERE id=? AND user_id=? AND status IN ('PENDING', 'CONFIRMED')";

        try (Connection con = DBConnection.getConnection()) {
            if (con == null) return false;

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, bookingId);
                ps.setInt(2, userId);
                return ps.executeUpdate() > 0;
            }
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean updateBookingStatus(int bookingId, String status) {
        if (!"CONFIRMED".equals(status) && !"REJECTED".equals(status) && !"CANCELLED".equals(status)) {
            return false;
        }

        String sql = "UPDATE bookings SET status=? WHERE id=?";

        try (Connection con = DBConnection.getConnection()) {
            if (con == null) return false;

            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setString(1, status);
                ps.setInt(2, bookingId);
                return ps.executeUpdate() > 0;
            }
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public int countTotalBookings() {
        String sql = "SELECT COUNT(*) FROM bookings";
        try (Connection con = DBConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) return rs.getInt(1);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0;
    }

    public int countPendingBookings() {
        String sql = "SELECT COUNT(*) FROM bookings WHERE status='PENDING'";
        try (Connection con = DBConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) return rs.getInt(1);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0;
    }

    public double calculateTotalRevenue() {
        String sql = "SELECT COALESCE(SUM(amount), 0) FROM payments WHERE payment_status='SUCCESS'";
        try (Connection con = DBConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) return rs.getDouble(1);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0.0;
    }

    private Booking mapBooking(ResultSet rs) throws SQLException {
        Booking booking = new Booking();
        booking.setId(rs.getInt("id"));
        booking.setUserId(rs.getInt("user_id"));
        booking.setVehicleId(rs.getInt("vehicle_id"));
        booking.setStartDate(rs.getDate("start_date"));
        booking.setEndDate(rs.getDate("end_date"));
        booking.setTotalAmount(rs.getDouble("total_amount"));
        booking.setStatus(rs.getString("status"));
        return booking;
    }
}
