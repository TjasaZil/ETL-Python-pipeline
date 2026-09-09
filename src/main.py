# Automating ETL Process wth Python
import pandas as pd
import logging

from src.functions.extract import extract_data
from src.functions.validate import check_for_null, validate_email, validate_date, validate_customers, validate_products, validate_orders
from src.functions.report import add_rejection_reasons, save_invalid_data, create_report, save_report
from country_codes import country_codes

#setup logging

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

# flow: laod data -> trim whitespace -> standardize country, -> transform dates -> float to int -> validate

# 1. extracting data

customers_path="../data/customers.csv"
orders_path="../data/orders.csv"
products_path = "../data/products.csv"
customers_invalid_path ="../output/invalid/customers_invalid.csv"
orders_invalid_path ="../output/invalid/orders_invalid.csv"
products_invalid_path ="../output/invalid/products_invalid.csv"
customers_report_path ="../output/reports/customers_report.json"
orders_report_path ="../output/reports/orders_report.json"
products_report_path ="../output/reports/products_report.json"

customers_df = extract_data(customers_path)
products_df = extract_data(products_path)
orders_df = extract_data(orders_path)

#print(validate_date(customers_df, 'created_at'))
#print(validate_customers(customers_df))
#print(validate_products(products_df))
#print(validate_orders(orders_df))
#invalid_customer_data=add_rejection_reasons(customers_df, validate_customers(customers_df))
#invalid_orders_data = add_rejection_reasons(orders_df, validate_orders(orders_df))
#invalid_products_data = add_rejection_reasons(products_df, validate_products(products_df))
#save_invalid_data(invalid_customer_data, customers_invalid_path)
#save_invalid_data(invalid_orders_data, orders_invalid_path)
#save_invalid_data(invalid_products_data, products_invalid_path)
#customers_report=create_report(customers_df, validate_customers(customers_df))
#save_report(customers_report, customers_report_path)
#products_report=create_report(products_df, validate_products(products_df))
#save_report(products_report, products_report_path)
#orders_report=create_report(orders_df, validate_orders(orders_df))
#save_report(orders_report, orders_report_path)
# 2. transform the data

# 3. clean / validate the data


#4. load the data into the database

