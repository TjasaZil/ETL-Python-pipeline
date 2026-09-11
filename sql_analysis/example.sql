-- Top 10 most ordered products of all time

SELECT o.product_id, p.name, sum(o.quantity) AS total_quantity
FROM orders AS o
LEFT JOIN products AS p
ON o.product_id = p.product_id
GROUP BY o.product_id, p.name
ORDER BY total_quantity DESC
LIMIT 10;

-- Which customers have placed the most orders?

SELECT c.name, count(o.order_id) as total_orders
FROM customers as c
join orders as o
on o.customer_id = c.customer_id
group by c.customer_id, c.name
order by total_orders desc;

-- What is the total quantity sold for each product?
-- select o.product_id, p.name, sum(quantity) as quantity_sold
-- from orders as o
-- left join products as p
-- on o.product_id = p.product_id
-- group by o.product_id, p.name

-- What is the total revenue by product category

-- select a.category, round(sum(a.item_order_price), 2) as total_category_price
-- from
--     (
--     select p.name, p.category, (o.quantity) * p.price as item_order_price
--     from orders as o
--     left join products as p
--     on p.product_id = o.product_id
--     ) as a
-- group by a.category
-- order by total_category_price desc

-- Which customers generated the highest revenue

-- How many orders were placed each day?

-- Which products have never been ordered?

-- which month were the most customers 'created'
-- which countries are most customers from?
-- ratio between food and non food items ordered