-- Verification output from bigbasket_capstone.db
-- products: 31
-- customers: 50
-- orders: 500
-- category_targets: 6
-- status counts: Cancelled 42, Delivered 434, Pending 24

SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products;
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers;
SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM orders;
SELECT 'category_targets' AS table_name, COUNT(*) AS row_count FROM category_targets;
SELECT status, COUNT(*) AS order_count FROM orders GROUP BY status ORDER BY status;
