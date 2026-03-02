-- Automated Electronics Laboratory Management System
-- Database Schema

CREATE DATABASE IF NOT EXISTS lab_management;
USE lab_management;

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    department VARCHAR(50),
    year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Staff Table
CREATE TABLE IF NOT EXISTS staff (
    staff_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'lab_assistant') DEFAULT 'lab_assistant',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Equipment Table
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    model_number VARCHAR(50),
    total_quantity INT NOT NULL DEFAULT 0,
    available_quantity INT NOT NULL DEFAULT 0,
    condition_status ENUM('good', 'fair', 'damaged') DEFAULT 'good',
    location VARCHAR(100),
    added_date DATE,
    INDEX idx_category (category),
    INDEX idx_condition (condition_status)
);

-- Experiments Table
CREATE TABLE IF NOT EXISTS experiments (
    experiment_id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_name VARCHAR(150) NOT NULL,
    description TEXT,
    required_equipment TEXT,
    duration_hours INT DEFAULT 2
);

-- Issue Records Table
CREATE TABLE IF NOT EXISTS issue_records (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    equipment_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    issue_date DATETIME NOT NULL,
    expected_return_date DATE NOT NULL,
    actual_return_date DATETIME,
    issued_by VARCHAR(20) NOT NULL,
    status ENUM('issued', 'returned', 'overdue') DEFAULT 'issued',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE,
    FOREIGN KEY (issued_by) REFERENCES staff(staff_id),
    INDEX idx_status (status),
    INDEX idx_student (student_id)
);

-- Maintenance Records Table
CREATE TABLE IF NOT EXISTS maintenance_records (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT NOT NULL,
    reported_by VARCHAR(20) NOT NULL,
    issue_description TEXT NOT NULL,
    reported_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    repair_date DATETIME,
    status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    cost DECIMAL(10, 2) DEFAULT 0.00,
    notes TEXT,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE,
    FOREIGN KEY (reported_by) REFERENCES staff(staff_id),
    INDEX idx_status (status)
);

-- Insert default admin user (password: admin123)
INSERT INTO staff (staff_id, name, email, password_hash, role) 
VALUES ('ADMIN001', 'System Administrator', 'admin@lab.edu', 
        'pbkdf2:sha256:260000$8xKZJ5Z5$e8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8', 
        'admin')
ON DUPLICATE KEY UPDATE staff_id=staff_id;

-- Insert sample equipment
INSERT INTO equipment (name, category, model_number, total_quantity, available_quantity, condition_status, location, added_date) VALUES
('Digital Multimeter', 'Measuring Instruments', 'DT-830B', 15, 15, 'good', 'Cabinet A1', CURDATE()),
('Oscilloscope', 'Measuring Instruments', 'DSO-X 2024A', 5, 5, 'good', 'Bench 1-5', CURDATE()),
('Function Generator', 'Signal Generators', 'AFG-2225', 8, 8, 'good', 'Bench 1-8', CURDATE()),
('Breadboard', 'Components', 'BB-830', 30, 30, 'good', 'Cabinet B2', CURDATE()),
('Power Supply', 'Power Sources', 'PS-305D', 10, 10, 'good', 'Bench 1-10', CURDATE()),
('Logic Analyzer', 'Testing Equipment', 'LA-2016', 3, 3, 'good', 'Cabinet A3', CURDATE()),
('Soldering Station', 'Tools', 'SS-936D', 12, 12, 'good', 'Workbench Area', CURDATE()),
('IC Tester', 'Testing Equipment', 'ICT-500', 4, 4, 'good', 'Cabinet A2', CURDATE()),
('Resistor Kit', 'Components', 'RK-1000', 20, 20, 'good', 'Cabinet B1', CURDATE()),
('Capacitor Kit', 'Components', 'CK-500', 20, 20, 'good', 'Cabinet B1', CURDATE())
ON DUPLICATE KEY UPDATE name=name;

-- Insert sample students
INSERT INTO students (student_id, name, email, phone, department, year) VALUES
('ECE2021001', 'Rahul Kumar', 'rahul.kumar@student.edu', '9876543210', 'Electronics', 3),
('ECE2021002', 'Priya Sharma', 'priya.sharma@student.edu', '9876543211', 'Electronics', 3),
('ECE2022001', 'Amit Patel', 'amit.patel@student.edu', '9876543212', 'Electronics', 2),
('CSE2021001', 'Sneha Reddy', 'sneha.reddy@student.edu', '9876543213', 'Computer Science', 3),
('EEE2022001', 'Vikram Singh', 'vikram.singh@student.edu', '9876543214', 'Electrical', 2)
ON DUPLICATE KEY UPDATE student_id=student_id;

-- Insert sample experiments
INSERT INTO experiments (experiment_name, description, required_equipment, duration_hours) VALUES
('RC Circuit Analysis', 'Study of charging and discharging of capacitors', 'Oscilloscope, Function Generator, Breadboard, Resistor Kit, Capacitor Kit', 3),
('Diode Characteristics', 'Study of forward and reverse bias characteristics of diodes', 'Power Supply, Multimeter, Breadboard, Resistor Kit', 2),
('Transistor Amplifier', 'Design and testing of common emitter amplifier', 'Oscilloscope, Function Generator, Power Supply, Breadboard', 3),
('Logic Gates', 'Implementation and verification of basic logic gates', 'IC Tester, Power Supply, Breadboard, Logic Analyzer', 2)
ON DUPLICATE KEY UPDATE experiment_name=experiment_name;
