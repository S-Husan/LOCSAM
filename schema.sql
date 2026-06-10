-- =============================================================================
-- LOCSAM Database Schema
-- Smart Tourism Management System for Samarkand, Uzbekistan
-- =============================================================================
-- HOW TO USE:
--   1. Install MySQL Server (https://dev.mysql.com/downloads/mysql/)
--   2. Open MySQL Workbench or command line: mysql -u root -p
--   3. Run this entire file: SOURCE path/to/schema.sql;
--   4. Install Python driver: python -m pip install mysql-connector-python
--   5. Set credentials in database.py or environment variables (see DATABASE_SETUP.md)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS locsam_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE locsam_db;

-- -----------------------------------------------------------------------------
-- Users (tourist accounts)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- Admins
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- Tourist locations
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'Monument',
    city VARCHAR(100) NOT NULL DEFAULT 'Samarkand, Uzbekistan',
    description TEXT NOT NULL,
    rating DECIMAL(3,1) NOT NULL DEFAULT 4.0,
    reviews INT NOT NULL DEFAULT 0,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    open_time VARCHAR(80) NOT NULL DEFAULT '06:00 AM - 09:00 PM',
    latitude DECIMAL(10,6) NOT NULL,
    longitude DECIMAL(10,6) NOT NULL,
    image VARCHAR(255) NOT NULL COMMENT 'Main cover image filename (without extension)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_locations_category (category),
    INDEX idx_locations_name (name)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- Gallery images (3 per location recommended)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS gallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL COMMENT 'Filename key e.g. registan_1',
    sort_order TINYINT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    INDEX idx_gallery_location (location_id)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- Ticket bookings
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location_id INT NOT NULL,
    ticket_type VARCHAR(50) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    total_price DECIMAL(10,2) NOT NULL,
    visit_date VARCHAR(50) NOT NULL,
    visit_time VARCHAR(20) DEFAULT '10:00 AM',
    status ENUM('upcoming', 'approved', 'cancelled', 'history') NOT NULL DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    INDEX idx_tickets_user (user_id),
    INDEX idx_tickets_status (status)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- User favorites
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, location_id)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- Reviews
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location_id INT NOT NULL,
    rating DECIMAL(3,1) NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    INDEX idx_reviews_location (location_id)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- Contact / support messages
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- App settings (per-user preferences — optional when using JSON store)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_settings (
    user_id INT PRIMARY KEY,
    language ENUM('en', 'uz', 'ru') NOT NULL DEFAULT 'en',
    dark_mode BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- Default admin account
-- Password: admin123 (hash in production!)
-- -----------------------------------------------------------------------------
INSERT INTO admins (username, password)
SELECT 'admin', 'admin123'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM admins WHERE username = 'admin');

-- -----------------------------------------------------------------------------
-- Sample Samarkand locations
-- -----------------------------------------------------------------------------
INSERT INTO locations (name, category, city, description, rating, reviews, price, open_time, latitude, longitude, image)
SELECT * FROM (
    SELECT 'Registan Square', 'Monument', 'Samarkand, Uzbekistan',
      'Registan Square is the heart of Samarkand and one of the most magnificent squares in the world.',
      4.8, 230, 10.00, '06:00 AM - 09:00 PM', 39.654200, 66.974700, 'registan'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM locations WHERE name = 'Registan Square');

INSERT INTO locations (name, category, city, description, rating, reviews, price, open_time, latitude, longitude, image)
SELECT * FROM (
    SELECT 'Shah-i-Zinda', 'Monument', 'Samarkand, Uzbekistan',
      'A famous necropolis with beautifully decorated mausoleums.',
      4.7, 180, 5.00, '06:00 AM - 09:00 PM', 39.662200, 66.979700, 'shah_i_zinda'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM locations WHERE name = 'Shah-i-Zinda');

INSERT INTO locations (name, category, city, description, rating, reviews, price, open_time, latitude, longitude, image)
SELECT * FROM (
    SELECT 'Bibi-Khanym Mosque', 'Mosque', 'Samarkand, Uzbekistan',
      'One of the largest mosques in Central Asia built by Amir Timur.',
      4.6, 150, 5.00, '06:00 AM - 09:00 PM', 39.660500, 66.979000, 'bibi_khanym'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM locations WHERE name = 'Bibi-Khanym Mosque');

INSERT INTO locations (name, category, city, description, rating, reviews, price, open_time, latitude, longitude, image)
SELECT * FROM (
    SELECT 'Amir Temur Mausoleum', 'Monument', 'Samarkand, Uzbekistan',
      'The final resting place of Amir Timur.',
      4.9, 210, 8.00, '06:00 AM - 09:00 PM', 39.648600, 66.969700, 'amir_temur'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM locations WHERE name = 'Amir Temur Mausoleum');

INSERT INTO locations (name, category, city, description, rating, reviews, price, open_time, latitude, longitude, image)
SELECT * FROM (
    SELECT 'Ulughbek Observatory', 'Museum', 'Samarkand, Uzbekistan',
      'An observatory established by Ulughbek.',
      4.5, 120, 5.00, '06:00 AM - 09:00 PM', 39.674700, 66.996700, 'ulughbek'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM locations WHERE name = 'Ulughbek Observatory');

INSERT INTO locations (name, category, city, description, rating, reviews, price, open_time, latitude, longitude, image)
SELECT * FROM (
    SELECT 'Tillya-Kori Madrasah', 'Museum', 'Samarkand, Uzbekistan',
      'Known for its stunning golden interior.',
      4.7, 170, 6.00, '06:00 AM - 09:00 PM', 39.654500, 66.975000, 'tillya_kori'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM locations WHERE name = 'Tillya-Kori Madrasah');

-- Demo user (password: password123)
INSERT INTO users (full_name, email, password)
SELECT 'Azizbek Abdurahmonov', 'azizbek@example.com', 'password123'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'azizbek@example.com');
