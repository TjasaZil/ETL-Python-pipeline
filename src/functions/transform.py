import pandas as pd
import logging
from ..country_codes import country_codes

#setup logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Changes the full country name to the ISO3166 code
def iso_country_code(df):
    try:
        df["country"] = df["country"].map(country_codes)
        return df
    except Exception as e:
        logger.exception(f"There was an error when changing the country code of the data: {e}")

#standardizes the date format
def standardize_date_format(df, column):
    try:
        df[column] = pd.to_datetime(df[column], dayfirst=True, format="%d/%m/%Y")
        return df
    except Exception as e:
        logger.exception(f"There was an error when changing the date format of the data: {e}")

#trims whitespace from certain columns and formats the string
def trim_whitespace(df, col):
    try:
        df[col] = df[col].str.split().str.join(" ").str.title()
        return df
    except Exception as e:
        logger.exception(f"There was an error when trimming the whitespace of the data: {e}")

#transform mail top lower case
def lowercase_email(df):
    try:
        for col in df.columns:
            if col == 'email':
                df[col] = df[col].str.lower()
        return df
    except Exception as e:
        logger.exception(f"There was an error when lowercase the string of the data: {e}")
# change ids from floats to inst
def float_to_int(df, col):
    try:
        df[col]=df[col].astype(int)
        return df
    except Exception as e:
        logger.exception(f"There was an error when changing the data type from float to int: {e}")


def transform_customers(df):
    try:
        df = standardize_date_format(df, column = "created_at")
        df = trim_whitespace(df, col="name")
        df = trim_whitespace(df, col="country")
        df = iso_country_code(df)
        df = lowercase_email(df)
        df = float_to_int(df, col="customer_id")
        return df
    except Exception as e:
        logger.exception(f"There was an error when transforming the customer data: {e}")

def transform_products(df):
    try:
        df = trim_whitespace(df, col="name")
        df = trim_whitespace(df, col="category")
        df = float_to_int(df, col="product_id")
        return df
    except Exception as e:
        logger.exception(f"There was an error when transforming the product data: {e}")

def transform_orders(df):
    try:
        df = float_to_int(df, col="order_id")
        df = float_to_int(df, col="customer_id")
        df = float_to_int(df, col="product_id")
        df = float_to_int(df, col="quantity")
        return df
    except Exception as e:
        logger.exception(f"There was an error when transforming the order data: {e}")