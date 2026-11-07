-- ========================================================
-- Vehicle Rental System - MySQL Database Schema & Seed Data
-- ========================================================

CREATE DATABASE IF NOT EXISTS rental_vehicle;
USE rental_vehicle;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'USER'
);

-- 2. Vehicles Table
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(50) NOT NULL UNIQUE,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    type VARCHAR(30) NOT NULL,
    price_per_day DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'AVAILABLE'
);

-- 3. Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    CONSTRAINT fk_booking_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_booking_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);

-- 4. Payments Table
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_booking FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);

-- ========================================================
-- Seed Data
-- ========================================================

-- Insert Default Admin (Password: admin123) and Customer (Password: user1234)
INSERT INTO users (name, email, password, role)
VALUES 
    ('System Administrator', 'admin@rental.com', '$2a$10$cQ6fW6YuKOdjOJcsvt.mve24kXCW/0GeFluq3l5K3sD7sQfy3rsyK', 'ADMIN'),
    ('John Customer', 'user@rental.com', '$2a$10$brtC9djlbjleAkw9mYgkPOCbGQXeFhX2cl9TBn6JkHOPynjHFV0yK', 'USER')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Insert Initial Fleet Vehicles
INSERT INTO vehicles (vehicle_number, brand, model, type, price_per_day, status)
VALUES
    ('AP39AB1234', 'Maruti', 'Swift', 'Hatchback', 1500.00, 'AVAILABLE'),
    ('AP39CD5678', 'Hyundai', 'Creta', 'SUV', 2500.00, 'AVAILABLE'),
    ('TS09EF9012', 'Honda', 'City', 'Sedan', 2200.00, 'AVAILABLE'),
    ('KA01GH3456', 'Toyota', 'Fortuner', 'SUV', 4500.00, 'AVAILABLE'),
    ('MH12JK7890', 'Royal Enfield', 'Hunter 350', 'Bike', 900.00, 'AVAILABLE')
ON DUPLICATE KEY UPDATE brand=VALUES(brand);
