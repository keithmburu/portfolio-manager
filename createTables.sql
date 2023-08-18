DROP DATABASE IF EXISTS TAPHK;
CREATE DATABASE IF NOT EXISTS TAPHK;
USE TAPHK;

CREATE TABLE portfolio (
    id INT PRIMARY KEY auto_increment,
    asset_type VARCHAR(255) NOT NULL,
    asset_ticker VARCHAR(20),
    asset_name VARCHAR(255) NOT NULL,
    amount_holding INT NOT NULL,
    buy_datetime DATETIME NOT NULL,
    mature_datetime DATETIME,
    currency VARCHAR(255)
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

CREATE TABLE historical_networth (
    id INT PRIMARY KEY auto_increment,
    date DATETIME NOT NULL,
    networth FLOAT NOT NULL
);

CREATE USER 'training'@'localhost' IDENTIFIED BY '1234567A';
GRANT ALL PRIVILEGES ON TAPHK TO 'training'@'localhost';

-- Insert CVS stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency, net_worth)
VALUES ('Stock', 'CVS', 'CVS Health Corporation', 100, '2023-08-18 09:00:00', NULL, 'USD', 15000.00);

-- Insert TESLA stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency, net_worth)
VALUES ('Stock', 'TSLA', 'Tesla, Inc.', 50, '2023-08-18 10:30:00', NULL, 'USD', 30000.00);

-- Insert GOOGLE stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency, net_worth)
VALUES ('Stock', 'GOOGL', 'Alphabet Inc.', 30, '2023-08-18 11:45:00', NULL, 'USD', 45000.00);

-- Insert MORGAN STANLEY stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency, net_worth)
VALUES ('Stock', 'MS', 'Morgan Stanley', 75, '2023-08-18 13:15:00', NULL, 'USD', 9000.00);

-- Insert WALMART stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency, net_worth)
VALUES ('Stock', 'WMT', 'Walmart Inc.', 40, '2023-08-18 14:30:00', NULL, 'USD', 6000.00);
