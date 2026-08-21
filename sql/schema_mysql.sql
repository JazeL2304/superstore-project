-- ============================================================================
-- Superstore Sales Database - MySQL Schema & DDL
-- Compatible with MySQL 5.7+ / MySQL 8.0+ / MariaDB
-- ============================================================================

CREATE DATABASE IF NOT EXISTS superstore_db;
USE superstore_db;

-- ----------------------------------------------------------------------------
-- Table structure for table `superstore`
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS superstore;

CREATE TABLE superstore (
    Row_ID INT NOT NULL PRIMARY KEY,
    Order_ID VARCHAR(25) NOT NULL,
    Order_Date DATE NOT NULL,
    Ship_Date DATE NOT NULL,
    Ship_Mode VARCHAR(25),
    Customer_ID VARCHAR(20) NOT NULL,
    Customer_Name VARCHAR(100),
    Segment VARCHAR(50),
    Country VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    Postal_Code VARCHAR(20),
    Region VARCHAR(20),
    Product_ID VARCHAR(30) NOT NULL,
    Category VARCHAR(50),
    Sub_Category VARCHAR(50),
    Product_Name VARCHAR(255),
    Sales DECIMAL(12, 4) NOT NULL DEFAULT 0.0000,
    Quantity INT NOT NULL DEFAULT 1,
    Discount DECIMAL(5, 4) NOT NULL DEFAULT 0.0000,
    Profit DECIMAL(12, 4) NOT NULL DEFAULT 0.0000,
    
    -- Performance Indexes for Analytical Queries
    INDEX idx_order_date (Order_Date),
    INDEX idx_region (Region),
    INDEX idx_category (Category),
    INDEX idx_sub_category (Sub_Category),
    INDEX idx_customer_id (Customer_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- MySQL Data Loading Command (via LOAD DATA LOCAL INFILE)
-- ----------------------------------------------------------------------------
-- LOAD DATA LOCAL INFILE '/path/to/Sample_-_Superstore.csv'
-- INTO TABLE superstore
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (Row_ID, Order_ID, @Order_Date, @Ship_Date, Ship_Mode, Customer_ID, Customer_Name, 
--  Segment, Country, City, State, Postal_Code, Region, Product_ID, Category, 
--  Sub_Category, Product_Name, Sales, Quantity, Discount, Profit)
-- SET 
--   Order_Date = STR_TO_DATE(@Order_Date, '%m/%d/%Y'),
--   Ship_Date  = STR_TO_DATE(@Ship_Date, '%m/%d/%Y');
