-- 01 Foundations

-- 1. SELECT / WHERE: orders from a specific city
SELECT o.order_id, c.city, o.order_date, o.amount_inr
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.customer_id
WHERE c.city = 'Mumbai';

-- 2. DISTINCT: every distinct category
SELECT DISTINCT category
FROM products
ORDER BY category;

-- 3. ORDER BY + LIMIT: five highest-value orders
SELECT order_id, amount_inr
FROM orders
ORDER BY amount_inr DESC
LIMIT 5;

-- 4. Alias (AS): aggregate renamed in output
SELECT status, COUNT(*) AS total_orders
FROM orders
GROUP BY status;

-- 5. IN: orders using either UPI or Credit Card
SELECT order_id, payment_mode, amount_inr
FROM orders
WHERE payment_mode IN ('UPI', 'Credit Card');

-- 6. BETWEEN: orders with amount from INR 100 through INR 300 inclusive
SELECT order_id, amount_inr
FROM orders
WHERE amount_inr BETWEEN 100 AND 300;

-- 7. NOT BETWEEN: orders outside INR 100 through INR 300 inclusive
SELECT order_id, amount_inr
FROM orders
WHERE amount_inr NOT BETWEEN 100 AND 300;

-- 8. IS NULL: orders with no rating (Cancelled/Pending)
SELECT order_id, status, rating
FROM orders
WHERE rating IS NULL;
