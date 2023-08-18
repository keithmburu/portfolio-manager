DROP DATABASE IF EXISTS TAPHK;
CREATE DATABASE IF NOT EXISTS TAPHK;
USE TAPHK;
CREATE USER IF NOT EXISTS 'training'@'localhost' IDENTIFIED BY '1234567A';
GRANT ALL PRIVILEGES ON TAPHK TO 'training'@'localhost';


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
    high_price FLOAT,
    low_price FLOAT
);

CREATE TABLE historical_networth (
    id INT PRIMARY KEY auto_increment,
    date DATETIME NOT NULL,
    networth FLOAT NOT NULL
);


-- Insert into the portfolio table
-- Insert TESLA stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency)
VALUES ('Stock', 'TSLA', 'Tesla, Inc.', 50, '2023-08-11 10:30:00', NULL, 'USD');

-- Insert GOOGLE stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency)
VALUES ('Stock', 'GOOGL', 'Alphabet Inc.', 30, '2023-08-11 11:45:00', NULL, 'USD');

-- Insert MORGAN STANLEY stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency)
VALUES ('Stock', 'MS', 'Morgan Stanley', 75, '2023-08-11 13:15:00', NULL, 'USD');

-- Insert WALMART stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency)
VALUES ('Stock', 'WMT', 'Walmart Inc.', 40, '2023-08-11 14:30:00', NULL, 'USD');

-- Insert CVS stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency)
VALUES ('Stock', 'CVS', 'CVS Health Corporation', 100, '2023-08-11 09:00:00', NULL, 'USD');

-- Display the portfolio table
SELECT * FROM portfolio;

-- Insert into the asset_data table
-- Insert CVS asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price)
VALUES ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-11 00:00:00', 80.25, 81.12, 82.18, 80.10),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-12 00:00:00', 81.50, 82.30, 83.45, 81.30),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-13 00:00:00', 82.40, 82.80, 83.90, 82.00),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-14 00:00:00', 82.70, 82.60, 83.20, 82.40),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-15 00:00:00', 82.50, 82.80, 83.10, 82.30),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-16 00:00:00', 82.70, 82.90, 83.30, 82.50),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-17 00:00:00', 82.80, 82.75, 83.00, 82.60);

-- Insert TESLA asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price)
VALUES ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-11 00:00:00', 710.25, 716.80, 720.50, 706.90),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-12 00:00:00', 718.50, 723.60, 728.20, 717.90),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-13 00:00:00', 724.00, 729.10, 732.40, 722.50),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-14 00:00:00', 727.80, 731.20, 734.10, 726.70),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-15 00:00:00', 731.50, 735.50, 738.20, 728.80),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-16 00:00:00', 735.20, 739.80, 742.60, 732.70),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-17 00:00:00', 740.00, 743.90, 746.80, 737.50);

-- Insert GOOGLE asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price)
VALUES ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-11 00:00:00', 128.50, 129.75, 130.20, 128.00),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-12 00:00:00', 129.80, 130.10, 130.70, 129.20),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-13 00:00:00', 130.15, 130.40, 130.90, 129.80),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-14 00:00:00', 130.30, 130.60, 131.00, 130.10),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-15 00:00:00', 130.50, 130.80, 131.20, 130.40),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-16 00:00:00', 130.70, 131.00, 131.40, 130.60),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-17 00:00:00', 130.90, 131.20, 131.60, 130.80);


-- Insert MORGAN STANLEY asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price)
VALUES ('Stock', 'MS', 'Morgan Stanley', '2023-08-11 00:00:00', 96.75, 97.10, 98.20, 96.40),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-12 00:00:00', 97.30, 97.50, 98.10, 97.00),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-13 00:00:00', 97.70, 98.00, 98.50, 97.20),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-14 00:00:00', 97.90, 98.20, 98.60, 97.50),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-15 00:00:00', 98.10, 98.40, 98.80, 97.70),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-16 00:00:00', 98.30, 98.60, 99.00, 98.10),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-17 00:00:00', 98.70, 98.80, 99.10, 98.40);

-- Insert WALMART asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price)
VALUES ('Stock', 'WMT', 'Walmart Inc.', '2023-08-11 00:00:00', 140.50, 141.20, 141.80, 140.10),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-12 00:00:00', 141.60, 141.80, 142.30, 141.10),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-13 00:00:00', 142.00, 142.40, 142.90, 141.70),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-14 00:00:00', 142.30, 142.60, 142.90, 142.10),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-15 00:00:00', 142.70, 143.00, 143.40, 142.50),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-16 00:00:00', 143.20, 143.50, 143.80, 142.90),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-17 00:00:00', 143.60, 143.70, 143.90, 143.30);

-- Display the asset_data table
SELECT * FROM asset_data;

-- Calculate and insert historical net worth
INSERT INTO historical_networth (date, networth)
SELECT ad.date, SUM(p.amount_holding * ad.close_price) AS networth
FROM asset_data ad
JOIN portfolio p ON ad.asset_name = p.asset_name
GROUP BY ad.date;

-- Display the calculated historical net worth
SELECT * FROM historical_networth;
