# Automating ETL Process wth Python
import pandas as pd
import logging
from src.pipelines.customers import customers_pipeline
from src.pipelines.products import products_pipeline
from src.pipelines.orders import orders_pipeline
customers_path="../data/customers.csv"
orders_path="../data/orders.csv"
products_path = "../data/products.csv"

#print(customers_pipeline(customers_path))
#print(products_pipeline(products_path))
print(orders_pipeline(orders_path))


