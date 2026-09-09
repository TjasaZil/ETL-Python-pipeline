# Automating ETL Process wth Python
import pandas as pd
import logging

from src.functions.extract import extract_data
from src.functions.validate import check_for_null, validate_email, validate_date, validate_customers, validate_products, validate_orders

from country_codes import country_codes

#setup logging

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

# flow: laod data -> trim whitespace -> standardize country, -> transform dates -> float to int -> validate

# 1. extracting data

customers_path="../data/customers.csv"
orders_path="../data/orders.csv"
products_path = "../data/products.csv"

customers_df = extract_data(customers_path)
products_df = extract_data(products_path)
orders_df = extract_data(orders_path)

#print(validate_date(customers_df, 'created_at'))
#print(validate_customers(customers_df))
#print(validate_products(products_df))
#print(validate_orders(orders_df))
# 2. transform the data

# 3. clean / validate the data


#4. load the data into the database

