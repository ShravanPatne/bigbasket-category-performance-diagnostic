-- 03 Reporting

-- (a) CASE WHEN tiering by Delivered revenue per product
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(CASE WHEN o.status = 'Delivered' THEN o.amount_inr ELSE 0 END) AS total_revenue
    FROM products AS p
    LEFT JOIN orders AS o ON p.product_id = o.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT
    product_id,
    product_name,
    category,
    total_revenue,
    CASE
        WHEN total_revenue >= 3000 THEN 'High'
        WHEN total_revenue >= 1000 THEN 'Medium'
        ELSE 'Low'
    END AS revenue_tier
FROM product_revenue
ORDER BY total_revenue DESC;

-- (b) Monthly-by-category business report, Delivered only
SELECT
    p.category AS category,
    strftime('%Y-%m', o.order_date) AS month,
    COUNT(*) AS order_count,
    SUM(o.amount_inr) AS total_revenue,
    AVG(o.amount_inr) AS avg_revenue
FROM orders AS o
INNER JOIN products AS p ON o.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category, strftime('%Y-%m', o.order_date)
ORDER BY p.category, month;

-- (c) Category target variance and three-way target status
WITH category_revenue AS (
    SELECT
        p.category,
        SUM(o.amount_inr) AS total_revenue
    FROM orders AS o
    INNER JOIN products AS p ON o.product_id = p.product_id
    WHERE o.status = 'Delivered'
    GROUP BY p.category
)
SELECT
    cr.category,
    cr.total_revenue,
    ct.target_revenue_inr,
    ct.target_revenue_inr - cr.total_revenue AS variance,
    ((cr.total_revenue - ct.target_revenue_inr) * 100.0) / ct.target_revenue_inr AS percentage_variance,
    CASE
        WHEN cr.total_revenue >= ct.target_revenue_inr THEN 'Above Target'
        WHEN (ct.target_revenue_inr - cr.total_revenue) <= 0.15 * ct.target_revenue_inr THEN 'Below Target - Watch'
        ELSE 'Below Target - Critical'
    END AS target_status
FROM category_revenue AS cr
INNER JOIN category_targets AS ct ON cr.category = ct.category
ORDER BY cr.total_revenue DESC;
