import pandas as pd
import logging
import csv
import re
from src.functions.transform import standardize_date_format

#setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#removing null values and writing them into their own file
def check_for_null(df):
    try:
        for index, row in df.iterrows():
            if row.isnull().values.any():
                df.dropna(inplace=True)
        logger.info(f"Checked for null values and removed them from the dataframe.")
        return df
    except Exception as e:
        logger.error(f" There was a problem when checking for null values: {e}")


#validating email
def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, str(email)))

def validate_email(df):
    try:
        df = df[df["email"].apply(is_valid_email)]
        logger.info(f"Checked for valid emails and removed invalid emails from the dataframe.")
        return df
    except Exception as e:
        logger.error(f" There was a problem when trying to validate email: {e}")

#validating that the date is not in the future
def validate_date(df):
    standardized_date=standardize_date_format(df)
    try:
        current_date = pd.Timestamp.today()
        for col in standardized_date.columns:
            if col == 'created_at' or col == 'order_date':
                for index, value in standardized_date[col].items():
                    if value > current_date:
                        df.drop(index, inplace=True)
        logger.info(
                        f"Checked for valid date and removed invalid dates from the dataframe.")
        return df
    except Exception as e:
        logger.error(f" There was a problem when trying to validate date: {e}")

#removing duplicates
def remove_duplicates(df):
    try:
        df_invalid = df.duplicated()
        df_invalid_rows = df[df_invalid]
        df_invalid_rows.to_csv("../data/invalid_data/duplicates.csv", index=False)
        df = df[~df_invalid]
        logger.info(f"Removed duplicate rows from the dataframe. There were {len(df_invalid_rows)} rows removed")
        return df
    except Exception as e:
        logger.error(f" There was a problem when trying to remove duplicate rows: {e}")

#checks if price is >=0
def checker_for_price(number):
    return number < 0
def check_price(df):
    #checks if price is negative
    try:
        df = df[df["price"].apply(checker_for_price)]
        logger.info("Checking price was succesfull")
        return df
    except Exception as e:
        logger.error(f"There was an error when checking the price:{e}")

#checks if quantity is > 0
def check_for_quantity(number):
    return number <= 0
def check_quantity(df):
    try:
        df = df[df["quantity"].apply(checker_for_price)]
        logger.info("Checking quantity was succesfull")
        return df
    except Exception as e:
        logger.error(f"There was an error when checking the quantity: {e}")
