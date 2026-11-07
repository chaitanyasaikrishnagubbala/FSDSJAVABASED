package com.rental.model;

public class Vehicle {

    private int id;
    private String vehicleNumber;
    private String brand;
    private String model;
    private String type;
    private double pricePerDay;
    private String status;

    public Vehicle() {
    }

    public Vehicle(int id,String vehicleNumber,String brand,String model,String type,double pricePerDay,String status) {
        this.id=id;
        this.vehicleNumber=vehicleNumber;
        this.brand=brand;
        this.model=model;
        this.type=type;
        this.pricePerDay=pricePerDay;
        this.status=status;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id=id;
    }

    public String getVehicleNumber() {
        return vehicleNumber;
    }

    public void setVehicleNumber(String vehicleNumber) {
        this.vehicleNumber=vehicleNumber;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand=brand;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model=model;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type=type;
    }

    public double getPricePerDay() {
        return pricePerDay;
    }

    public void setPricePerDay(double pricePerDay) {
        this.pricePerDay=pricePerDay;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status=status;
    }

    public String getImageUrl() {
        if (model != null) {
            String m = model.toLowerCase();
            if (m.contains("swift")) return "images/vehicles/swift.jpg";
            if (m.contains("creta")) return "images/vehicles/creta.jpg";
            if (m.contains("city")) return "images/vehicles/city.jpg";
            if (m.contains("fortuner")) return "images/vehicles/fortuner.jpg";
            if (m.contains("hunter") || m.contains("enfield")) return "images/vehicles/hunter.jpg";
        }
        if (type != null) {
            String t = type.toLowerCase();
            if (t.contains("hatchback")) return "images/vehicles/hatchback.jpg";
            if (t.contains("suv")) return "images/vehicles/suv.jpg";
            if (t.contains("sedan")) return "images/vehicles/sedan.jpg";
            if (t.contains("bike") || t.contains("motorcycle") || t.contains("scooter")) return "images/vehicles/bike.jpg";
        }
        return "images/vehicles/default.jpg";
    }
}