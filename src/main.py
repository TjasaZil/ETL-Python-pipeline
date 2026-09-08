# Automating ETL Process wth Python
import pandas as pd
import logging

from src.functions.transform import iso_country_code, standardize_date_format, trim_whitespace, float_to_int
from src.functions.extract import extract_data
from src.functions.validate import check_for_null, validate_email, validate_date, remove_duplicates

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
#validate_date(customers_df)
#validate_email(customers_df)
remove_duplicates(customers_df)
print(customers_df)

# 2. transform the data

# 3. clean / validate the data


#4. load the data into the database

