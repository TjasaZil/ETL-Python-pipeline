CREATE TABLE customers (
    customer_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    country VARCHAR(3) NOT NULL,
    created_at DATE NOT NULL,

    PRIMARY KEY (customer_id)
);