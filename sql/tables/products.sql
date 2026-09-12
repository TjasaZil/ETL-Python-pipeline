CREATE TABLE products (
    product_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,

    PRIMARY KEY (product_id)
);