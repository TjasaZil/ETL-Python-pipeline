import pandas as pd
import logging
from ..country_codes import country_codes

#setup logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. transform the data

#Changes the full country name to the ISO3166 code
def iso_country_code(df):
    try:
        df["country"] = df["country"].map(country_codes)
        return df
    except Exception as e:
        logger.exception(f"There was an error when changing the country code of the data: {e}")

#standardizes the date format
def standardize_date_format(df):
    try:
        df["created_at"] = pd.to_datetime(df["created_at"], dayfirst=True, format="%d/%m/%Y")
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
def float_to_int(df):
    try:
        for col in df.columns:
            if col == 'customer_id' or col == 'product_id':
                pd.options.display.float_format = '{:,.0f}'.format
        return df
    except Exception as e:
        logger.exception(f"There was an error when changing the data type from float to int: {e}")