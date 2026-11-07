
package com.rental.dao;

import com.rental.model.Vehicle;
import com.rental.util.DBConnection;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class VehicleDAO {

    public boolean addVehicle(Vehicle vehicle) {
        String sql="INSERT INTO vehicles(vehicle_number,brand,model,type,price_per_day,status) VALUES(?,?,?,?,?,?)";

        try(Connection con=DBConnection.getConnection()) {
            if(con==null)return false;

            try(PreparedStatement ps=con.prepareStatement(sql)) {
                ps.setString(1,vehicle.getVehicleNumber());
                ps.setString(2,vehicle.getBrand());
                ps.setString(3,vehicle.getModel());
                ps.setString(4,vehicle.getType());
                ps.setDouble(5,vehicle.getPricePerDay());
                ps.setString(6,"AVAILABLE");
                return ps.executeUpdate()>0;
            }
        } catch(SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean updateVehicle(Vehicle vehicle) {
        String sql="UPDATE vehicles SET vehicle_number=?,brand=?,model=?,type=?,price_per_day=?,status=? WHERE id=?";

        try(Connection con=DBConnection.getConnection()) {
            if(con==null)return false;

            try(PreparedStatement ps=con.prepareStatement(sql)) {
                ps.setString(1,vehicle.getVehicleNumber());
                ps.setString(2,vehicle.getBrand());
                ps.setString(3,vehicle.getModel());
                ps.setString(4,vehicle.getType());
                ps.setDouble(5,vehicle.getPricePerDay());
                ps.setString(6,vehicle.getStatus());
                ps.setInt(7,vehicle.getId());
                return ps.executeUpdate()>0;
            }
        } catch(SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean deleteVehicle(int id) {
        String sql="DELETE FROM vehicles WHERE id=?";

        try(Connection con=DBConnection.getConnection()) {
            if(con==null)return false;

            try(PreparedStatement ps=con.prepareStatement(sql)) {
                ps.setInt(1,id);
                return ps.executeUpdate()>0;
            }
        } catch(SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public Vehicle getVehicleById(int id) {
        String sql="SELECT * FROM vehicles WHERE id=?";

        try(Connection con=DBConnection.getConnection()) {
            if(con==null)return null;

            try(PreparedStatement ps=con.prepareStatement(sql)) {
                ps.setInt(1,id);

                try(ResultSet rs=ps.executeQuery()) {
                    if(rs.next())return mapVehicle(rs);
                }
            }
        } catch(SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public List<Vehicle> getAllVehicles() {
        List<Vehicle> vehicles=new ArrayList<>();
        String sql="SELECT * FROM vehicles ORDER BY id DESC";

        try(Connection con=DBConnection.getConnection()) {
            if(con==null)return vehicles;

            try(PreparedStatement ps=con.prepareStatement(sql);
                ResultSet rs=ps.executeQuery()) {

                while(rs.next())vehicles.add(mapVehicle(rs));
            }
        } catch(SQLException e) {
            e.printStackTrace();
        }
        return vehicles;
    }

    public List<Vehicle> getAvailableVehicles() {
        List<Vehicle> vehicles=new ArrayList<>();
        String sql="SELECT * FROM vehicles WHERE status='AVAILABLE' ORDER BY id DESC";

        try(Connection con=DBConnection.getConnection()) {
            if(con==null)return vehicles;

            try(PreparedStatement ps=con.prepareStatement(sql);
                ResultSet rs=ps.executeQuery()) {

                while(rs.next())vehicles.add(mapVehicle(rs));
            }
        } catch(SQLException e) {
            e.printStackTrace();
        }
        return vehicles;
    }

    public int countTotalVehicles() {
        String sql = "SELECT COUNT(*) FROM vehicles";
        try (Connection con = DBConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) return rs.getInt(1);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0;
    }

    public int countAvailableVehicles() {
        String sql = "SELECT COUNT(*) FROM vehicles WHERE status='AVAILABLE'";
        try (Connection con = DBConnection.getConnection();
             PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) return rs.getInt(1);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0;
    }

    private Vehicle mapVehicle(ResultSet rs) throws SQLException {
        Vehicle vehicle=new Vehicle();
        vehicle.setId(rs.getInt("id"));
        vehicle.setVehicleNumber(rs.getString("vehicle_number"));
        vehicle.setBrand(rs.getString("brand"));
        vehicle.setModel(rs.getString("model"));
        vehicle.setType(rs.getString("type"));
        vehicle.setPricePerDay(rs.getDouble("price_per_day"));
        vehicle.setStatus(rs.getString("status"));
        return vehicle;
    }
}

