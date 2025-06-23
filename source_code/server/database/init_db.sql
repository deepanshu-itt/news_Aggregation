CREATE DATABASE IF NOT EXISTS news_aggregator_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE news_aggregator_db;

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    is_hidden BOOLEAN NOT NULL DEFAULT FALSE
);

-- Table for Users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for External API Servers (e.g., NewsAPI.org, TheNewsAPI.com)
CREATE TABLE IF NOT EXISTS external_servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    api_key VARCHAR(255) NOT NULL,
    base_url VARCHAR(512) NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for News Articles
CREATE TABLE IF NOT EXISTS news_articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    url VARCHAR(512) UNIQUE NOT NULL,
    image_url VARCHAR(512),
    published_at DATETIME,
    source VARCHAR(255),
    category_id INT,
    raw_data JSON, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_hidden BOOLEAN NOT NULL DEFAULT FALSE,
    report_count INT NOT NULL DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Table for Users' Saved Articles (Many-to-Many relationship)
CREATE TABLE IF NOT EXISTS saved_articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    article_id INT NOT NULL,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (user_id, article_id) 
    FOREIGN KEY (article_id) REFERENCES news_articles(id) ON DELETE CASCADE

);

-- Table for User Notification Preferences
CREATE TABLE IF NOT EXISTS user_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE, 
    email_enabled BOOLEAN DEFAULT TRUE,
    daily_digest_enabled BOOLEAN DEFAULT FALSE,
    category_preferences JSON,
    email VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Populate initial categories (INSERT IGNORE is crucial here)
INSERT IGNORE INTO categories (name) VALUES ('Business');
INSERT IGNORE INTO categories (name) VALUES ('Entertainment');
INSERT IGNORE INTO categories (name) VALUES ('Sports');
INSERT IGNORE INTO categories (name) VALUES ('Technology');
INSERT IGNORE INTO categories (name) VALUES ('Health');
INSERT IGNORE INTO categories (name) VALUES ('Science');
INSERT IGNORE INTO categories (name) VALUES ('Politics');
INSERT IGNORE INTO categories (name) VALUES ('General');

-- Add a default admin user for testing (CHANGE PASSWORD IN PRODUCTION!)
INSERT IGNORE INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@example.com', '$2b$12$DqXyJmH0xYxN.2/C2.B.O.vG.m.0.k.E.W.O.v.m.0.k.E.W.O.v.m.0.k.E.W.O.v', 'admin');
-- Password for 'admin' user above is 'password' (hashed with Werkzeug.security)
-- Generate your own hash for production!



CREATE TABLE IF NOT EXISTS email_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    article_ids JSON NOT NULL,  -- renamed and changed to JSON
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
    -- No FK for article_ids since it's now an array
);

CREATE TABLE IF NOT EXISTS article_reactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    article_id INT NOT NULL,
    reaction ENUM('like', 'dislike') NOT NULL,
    reacted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_article (user_id, article_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (article_id) REFERENCES news_articles(id)
);
