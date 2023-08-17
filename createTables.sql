DROP DATABASE IF EXISTS TAPHK;
CREATE DATABASE IF NOT EXISTS TAPHK;
USE TAPHK;

CREATE TABLE portfolio (
    id INT PRIMARY KEY auto_increment,
    asset_type VARCHAR(255) NOT NULL,
    asset_ticker VARCHAR(20),
    asset_name VARCHAR(255) NOT NULL,
    volume INT NOT NULL,
    start_datetime DATETIME NOT NULL,
    mature_datetime DATETIME,
    currency VARCHAR(255),
);


CREATE TABLE asset_data (
    id INT PRIMARY KEY auto_increment,
    asset_type VARCHAR(255) NOT NULL,
    asset_ticker VARCHAR(20),
    asset_name VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL,
    open_price FLOAT,
    close_price FLOAT,
    high_price,
    low_price
);

CREATE USER 'training'@'localhost' IDENTIFIED BY '1234567A';
GRANT ALL PRIVILEGES ON TAPHK TO 'training'@'localhost';