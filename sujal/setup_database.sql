-- MySQL Database Setup Script
-- Run this script in MySQL Workbench or MySQL Command Line

-- Create database
CREATE DATABASE IF NOT EXISTS number_guessing_game;

-- Use the database
USE number_guessing_game;

-- Create users table (this will also be created automatically by the Python app)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    best_score INT DEFAULT NULL
);

-- Optional: Create a dedicated user for the application (recommended for production)
-- Replace 'gameuser' and 'gamepassword' with your preferred credentials
-- CREATE USER 'gameuser'@'localhost' IDENTIFIED BY 'gamepassword';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON number_guessing_game.* TO 'gameuser'@'localhost';
-- FLUSH PRIVILEGES;

-- View existing tables
SHOW TABLES;

-- View table structure
DESCRIBE users;