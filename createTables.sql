DROP DATABASE TAPHK;
CREATE DATABASE TAPHK if not exists;
USE TAPHK;

CREATE TABLE porfolio (
    id INT PRIMARY KEY auto_increment,
    stock_ticker VARCHAR(20) NOT NULL,
    volume INT NOT NULL
);


CREATE TABLE stock_data (
    id INT PRIMARY KEY auto_increment,
    stock_ticker VARCHAR(20) NOT NULL,
    date DATETIME NOT NULL,
    open_price FLOAT NOT NULL,
    close_price FLOAT NOT NULL,
    high_price FLOAT NOT NULL,
    low_price FLOAT NOT NULL,
    volume INT NOT NULL
);