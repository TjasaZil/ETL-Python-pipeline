-- Top 10 most ordered products of all time
SELECT p.name, SUM(o.quantity) AS total_quantity
FROM orders AS o
JOIN products AS p
ON o.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY total_quantity DESC
LIMIT 10;

-- Which customers have placed the most orders?
SELECT c.name, COUNT(DISTINCT o.order_id) AS total_orders
FROM orders AS o
JOIN customers AS c
ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_orders DESC;

-- What is the total quantity sold for each product?
SELECT p.name, SUM(o.quantity) AS total_sold
FROM orders AS o
JOIN products AS p
ON p.product_id = o.product_id
GROUP BY p.product_id, p.name
ORDER BY total_sold DESC;

-- What is the total revenue by product category
 SELECT a.category, ROUND(SUM(a.item_order_price), 2) AS total_category_price
 FROM
     (
     SELECT p.name, p.category, (o.quantity * p.price) AS item_order_price
     FROM orders AS o
     LEFT JOIN products AS p
	 ON p.product_id = o.product_id
     ) AS a
GROUP BY a.category
ORDER BY total_category_price DESC;

-- Which customers generated the highest revenue
SELECT a.name, ROUND(sum(a.quantity * p.price), 2) as total_revenue
FROM
	(SELECT o.customer_id, c.name, o.product_id, sum(o.quantity) as quantity
	FROM orders AS o
	LEFT JOIN customers AS c
	ON c.customer_id = o.customer_id
	GROUP BY o.customer_id, c.name, o.product_id) AS a
LEFT JOIN products AS p
ON p.product_id = a.product_id
WHERE a.name IS NOT NULL
GROUP BY a.name
ORDER BY total_revenue DESC;

-- How many orders were placed each day?
SELECT a.order_date, COUNT(a.order_date) AS total_daily_orders
FROM
	(SELECT DISTINCT order_id, order_date
FROM orders
) AS a
GROUP BY a.order_date
ORDER BY total_daily_orders DESC;

-- Which products have never been ordered?

SELECT p.name AS never_ordered
FROM products AS p
LEFT JOIN orders AS o
ON o.product_id = p.product_id
WHERE o.product_id IS NULL;

-- which month were the most customers 'created'
SELECT MONTHNAME(created_at) AS created_month,  COUNT(*) AS total_created
FROM customers
GROUP BY created_month
ORDER BY total_created DESC;

-- which countries are most customers from?
SELECT country, COUNT(country) AS number_of_customers
FROM customers
GROUP BY country
ORDER BY number_of_customers DESC;