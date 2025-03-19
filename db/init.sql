-- Database initialization script
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(200) NOT NULL
);

-- Initial example data
INSERT INTO todos (task) VALUES ('Complete DevOps project');
INSERT INTO todos (task) VALUES ('Set up Prometheus monitoring');