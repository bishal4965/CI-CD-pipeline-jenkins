-- File: db/init.sql
-- MySQL initialization script
CREATE TABLE IF NOT EXISTS test (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255) NOT NULL
);

INSERT INTO test(message) VALUES('Database Initialized');
