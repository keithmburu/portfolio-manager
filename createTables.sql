DROP DATABASE IF EXISTS TAPHK;
DROP USER IF EXISTS 'training'@'localhost';

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
    currency VARCHAR(255),
    performance FLOAT
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
    low_price FLOAT,
    portfolio_id INT,
    FOREIGN KEY (portfolio_id) REFERENCES portfolio(id)
);

CREATE TABLE historical_networth (
    id INT PRIMARY KEY auto_increment,
    date DATETIME NOT NULL,
    networth FLOAT NOT NULL
);

CREATE TABLE asset_transactions (
    id INT PRIMARY KEY auto_increment,
    asset_id INT,
    transaction_type ENUM('BUY', 'SELL') NOT NULL,
    transaction_datetime DATETIME NOT NULL,
    transaction_amount INT NOT NULL,
    transaction_price FLOAT NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES portfolio(id)
);

-- Insert into the portfolio table
-- Insert TESLA stock data
INSERT INTO portfolio (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency,performance)
VALUES ('Stock', 'CVS', 'CVS Health Corporation', 100, '2023-08-11 00:00:00', NULL, 'USD', NULL),
        ('Stock', 'TSLA', 'Tesla, Inc.', 50, '2023-08-11 00:00:00', NULL, 'USD', NULL),
       ('Stock', 'GOOGL', 'Alphabet Inc.', 30, '2023-08-11 00:00:00', NULL, 'USD', NULL),
       ('Stock', 'MS', 'Morgan Stanley', 75, '2023-08-11 00:00:00', NULL, 'USD', NULL),
       ('Stock', 'WMT', 'Walmart Inc.', 40, '2023-08-11 00:00:00', NULL, 'USD', NULL);

-- Display the portfolio table
SELECT * FROM portfolio;

-- Insert all the buy actions into the asset_transaction table
INSERT INTO asset_transactions (asset_id, transaction_type, transaction_datetime,transaction_amount, transaction_price)
    VALUES (1, 'BUY', '2023-08-11 00:00:00',100, 81.12),
            (2, 'BUY', '2023-08-11 00:00:00',50, 716.80),
            (3, 'BUY', '2023-08-11 00:00:00',30, 131.20),
            (4, 'BUY', '2023-08-11 00:00:00',75,97.10),
            (5, 'BUY', '2023-08-11 00:00:00',40,141.20);
-- Display the portfolio table
SELECT * FROM asset_transactions;

-- Insert into the asset_data table
-- Insert CVS asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price,portfolio_id)
VALUES ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-11 00:00:00', 80.25, 81.12, 82.18, 80.10,1),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-12 00:00:00', 81.50, 82.30, 83.45, 81.30,1),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-13 00:00:00', 82.40, 82.80, 83.90, 82.00,1),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-14 00:00:00', 82.70, 82.60, 83.20, 82.40,1),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-15 00:00:00', 82.50, 82.80, 83.10, 82.30,1),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-16 00:00:00', 82.70, 82.90, 83.30, 82.50,1),
       ('Stock', 'CVS', 'CVS Health Corporation', '2023-08-17 00:00:00', 82.80, 82.75, 83.00, 82.60,1);

-- Insert TESLA asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price,portfolio_id)
VALUES ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-11 00:00:00', 710.25, 716.80, 720.50, 706.90,2),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-12 00:00:00', 718.50, 723.60, 728.20, 717.90,2),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-13 00:00:00', 724.00, 729.10, 732.40, 722.50,2),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-14 00:00:00', 727.80, 731.20, 734.10, 726.70,2),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-15 00:00:00', 731.50, 735.50, 738.20, 728.80,2),
       ('Stock', 'TSLA', 'Tela, Inc.', '2023-08-16 00:00:00', 735.20, 739.80, 742.60, 732.70,2),
       ('Stock', 'TSLA', 'Tesla, Inc.', '2023-08-17 00:00:00', 740.00, 743.90, 746.80, 737.50,2);

-- Insert GOOGLE asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price,portfolio_id)
VALUES ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-11 00:00:00', 130.90, 131.20, 131.60, 130.80,3),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-12 00:00:00', 129.80, 130.10, 130.70, 129.20,3),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-13 00:00:00', 130.15, 130.40, 130.90, 129.80,3),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-14 00:00:00', 130.30, 130.60, 131.00, 130.10,3),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-15 00:00:00', 130.50, 130.80, 131.20, 130.40,3),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-16 00:00:00', 130.70, 131.00, 131.40, 130.60,3),
       ('Stock', 'GOOGL', 'Alphabet Inc.', '2023-08-17 00:00:00', 128.50, 129.75, 130.20, 128.00,3);


-- Insert MORGAN STANLEY asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price,portfolio_id)
VALUES ('Stock', 'MS', 'Morgan Stanley', '2023-08-11 00:00:00', 96.75, 97.10, 98.20, 96.40,4),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-12 00:00:00', 97.30, 97.50, 98.10, 97.00,4),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-13 00:00:00', 97.70, 98.00, 98.50, 97.20,4),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-14 00:00:00', 97.90, 98.20, 98.60, 97.50,4),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-15 00:00:00', 98.10, 98.40, 98.80, 97.70,4),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-16 00:00:00', 98.30, 98.60, 99.00, 98.10,4),
       ('Stock', 'MS', 'Morgan Stanley', '2023-08-17 00:00:00', 98.70, 98.80, 99.10, 98.40,4);

-- Insert WALMART asset data
INSERT INTO asset_data (asset_type, asset_ticker, asset_name, date, open_price, close_price, high_price, low_price,portfolio_id)
VALUES ('Stock', 'WMT', 'Walmart Inc.', '2023-08-11 00:00:00', 140.50, 141.20, 141.80, 140.10,5),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-12 00:00:00', 141.60, 141.80, 142.30, 141.10,5),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-13 00:00:00', 142.00, 142.40, 142.90, 141.70,5),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-14 00:00:00', 142.30, 142.60, 142.90, 142.10,5),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-15 00:00:00', 142.70, 143.00, 143.40, 142.50,5),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-16 00:00:00', 143.20, 143.50, 143.80, 142.90,5),
       ('Stock', 'WMT', 'Walmart Inc.', '2023-08-17 00:00:00', 143.60, 143.70, 143.90, 143.30,5);

-- Display the asset_data table
SELECT * FROM asset_data;

-- Calculate and insert historical net worth
INSERT INTO historical_networth (date, networth)
SELECT ad.date, SUM(p.amount_holding * ad.close_price) AS networth
FROM asset_data ad
JOIN portfolio p ON ad.asset_name = p.asset_name
GROUP BY ad.date;

-- The calculated net worth and performance is based on the historical data
-- for the ease of our life, this portion of data is pre-calculate

-- Display the calculated historical net worth
SELECT * FROM historical_networth;

-- calculate the performance of each asset in the portfolio
UPDATE portfolio p
JOIN (
    SELECT 
        ad.asset_name, 
        ((ad.close_price - ad.buy_price) / ad.buy_price) * 100 AS performance
    FROM (
        SELECT 
            p.asset_name, 
            p.buy_datetime,
            ad.close_price,
            (SELECT open_price FROM asset_data WHERE asset_name = p.asset_name AND date = p.buy_datetime) AS buy_price
        FROM portfolio p
        JOIN asset_data ad ON p.asset_name = ad.asset_name
        WHERE ad.date = (SELECT MAX(date) FROM asset_data WHERE asset_name = p.asset_name)
    ) AS ad
) AS asset_performance ON p.asset_name = asset_performance.asset_name
SET p.performance = asset_performance.performance;


-- Display the updated portfolio table
SELECT * FROM portfolio;

CREATE USER 'training'@'localhost' IDENTIFIED BY '1234567A';
GRANT ALL PRIVILEGES ON TAPHK.* TO 'training'@'localhost';
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'training'@'localhost';
