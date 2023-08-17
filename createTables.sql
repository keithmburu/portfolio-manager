DROP DATABASE IF EXISTS TAPHK;
CREATE DATABASE IF NOT EXISTS TAPHK;
USE TAPHK;

CREATE TABLE portfolio (
    id INT PRIMARY KEY auto_increment,
    asset_type VARCHAR(255) NOT NULL,
    stock_ticker VARCHAR(20) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    volume INT NOT NULL,
    start_datetime DATETIME NOT NULL
);


CREATE TABLE asset_data (
    id INT PRIMARY KEY auto_increment,
    asset_type VARCHAR(255) NOT NULL,
    stock_ticker VARCHAR(20) NOT NULL,
    date DATETIME NOT NULL,
    open_price FLOAT NOT NULL,
    close_price FLOAT NOT NULL,
    high_price FLOAT NOT NULL,
    low_price FLOAT NOT NULL,
    volume INT NOT NULL
);

CREATE USER 'training'@'localhost' IDENTIFIED BY '1234567A';
GRANT ALL PRIVILEGES ON TAPHK TO 'training'@'localhost';