-- ============================================================================
-- Superstore Sales Analysis - SQL Queries
-- Databases: SQLite (superstore.db) & MySQL (superstore_db)
-- Table: superstore
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Pertanyaan Bisnis 1: Sub-kategori produk mana yang paling untung vs paling rugi?
-- Penjelasan: Mengagregasi Total Sales, Total Profit, Rata-rata Diskon, dan Profit Margin 
-- per Sub-Category untuk mengidentifikasi produk paling profitabel dan paling merugikan.
-- Dialect: ANSI SQL / Compatible with SQLite & MySQL
-- ----------------------------------------------------------------------------
SELECT 
    Sub_Category,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(AVG(Discount) * 100, 2) AS avg_discount_pct,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY Sub_Category
ORDER BY total_profit DESC;


-- ----------------------------------------------------------------------------
-- Pertanyaan Bisnis 2: Apakah diskon berpengaruh terhadap profit?
-- Penjelasan: Mengelompokkan transaksi berdasarkan bracket persentase diskon
-- untuk menganalisis dampak tingkat pemberian diskon terhadap profitabilitas rata-rata dan margin.
-- Dialect: ANSI SQL / Compatible with SQLite & MySQL
-- ----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN Discount = 0 THEN '1. No Discount (0%)'
        WHEN Discount > 0 AND Discount <= 0.2 THEN '2. Low Discount (1-20%)'
        WHEN Discount > 0.2 AND Discount <= 0.4 THEN '3. Moderate Discount (21-40%)'
        WHEN Discount > 0.4 AND Discount <= 0.6 THEN '4. High Discount (41-60%)'
        ELSE '5. Very High Discount (>60%)'
    END AS discount_bracket,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(AVG(Profit), 2) AS avg_profit_per_item,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY discount_bracket
ORDER BY discount_bracket ASC;


-- ----------------------------------------------------------------------------
-- Pertanyaan Bisnis 3: Bagaimana tren penjualan dari waktu ke waktu (bulanan)?
-- Penjelasan: Mengagregasi data bulanan untuk melihat tren Total Sales, Total Profit, dan Margin.
-- ----------------------------------------------------------------------------
-- [SQLite Version]
SELECT 
    strftime('%Y-%m', Order_Date) AS year_month,
    COUNT(DISTINCT Order_ID) AS total_orders,
    ROUND(SUM(Sales), 2) AS monthly_sales,
    ROUND(SUM(Profit), 2) AS monthly_profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY year_month
ORDER BY year_month ASC;

-- [MySQL Alternative Syntax]
-- SELECT 
--     DATE_FORMAT(Order_Date, '%Y-%m') AS year_month,
--     COUNT(DISTINCT Order_ID) AS total_orders,
--     ROUND(SUM(Sales), 2) AS monthly_sales,
--     ROUND(SUM(Profit), 2) AS monthly_profit,
--     ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS profit_margin_pct
-- FROM superstore
-- GROUP BY year_month
-- ORDER BY year_month ASC;


-- ----------------------------------------------------------------------------
-- Pertanyaan Bisnis 4: Wilayah (region) mana yang performanya paling baik?
-- Penjelasan: Mengagregasi per wilayah (Region) untuk melihat persebaran sales,
-- profitabilitas, dan margin profit antar region (West, East, Central, South).
-- Dialect: ANSI SQL / Compatible with SQLite & MySQL
-- ----------------------------------------------------------------------------
SELECT 
    Region,
    COUNT(DISTINCT Order_ID) AS total_orders,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY Region
ORDER BY total_profit DESC;


-- ----------------------------------------------------------------------------
-- Pertanyaan Bisnis 5: Siapa 10 customer dengan kontribusi profit tertinggi?
-- Penjelasan: Mengurutkan pelanggan berdasarkan akumulasi total profit terbesar 
-- yang mereka kontribusikan ke Superstore.
-- Dialect: ANSI SQL / Compatible with SQLite & MySQL
-- ----------------------------------------------------------------------------
SELECT 
    Customer_ID,
    Customer_Name,
    Segment,
    COUNT(DISTINCT Order_ID) AS total_orders,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY Customer_ID, Customer_Name, Segment
ORDER BY total_profit DESC
LIMIT 10;
