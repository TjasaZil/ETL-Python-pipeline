CREATE TABLE orders (
    order_id INT NOT NULL,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    order_date DATE NOT NULL,

    PRIMARY KEY (order_id, customer_id, product_id),

    FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
);