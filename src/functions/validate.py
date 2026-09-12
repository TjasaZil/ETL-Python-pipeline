import pandas as pd
import logging
import re

#setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#checking for null values
def check_for_null(df, column):
    try:
        return ~df[column].isnull()
    except Exception as e:
        logger.exception(f" There was a problem when checking for null values: {e}")


#validating email
def is_valid_email(email):
    pattern =  r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, str(email)))

def validate_email(df):
    try:
        return df["email"].apply(is_valid_email)
    except Exception as e:
        logger.exception(f" There was a problem when trying to validate email: {e}")


#validating that the date is not in the future and that the date is even a date
def validate_date(df, column):
    try:
        dates = pd.to_datetime(df[column], errors='coerce')
        current_date = pd.Timestamp.today()
        return dates.notna() & (dates <= current_date)
    except Exception as e:
        logger.exception(f" There was a problem when trying to validate date: {e}")

#removing duplicates - not whole row but user determening what are the duplicates
def validate_duplicates(df, column):
    try:
        return ~df.duplicated(subset=[column], keep=False)
    except Exception as e:
        logger.exception(f" There was a problem when trying to remove duplicate rows: {e}")


def validate_positives(df, column):
    try:
        return df[column].notna() & (df[column] > 0)
    except Exception as e:
        logger.exception(f"There was an error when checking the negative number:{e}")

#check if customer_id and product_id are valid in orders
def id_existing(df1, df2, column):
    try:
        valid_ids = df1[column].unique()
        return df2[column].isin(valid_ids)
    except Exception as e:
        logger.exception(f" There was a problem when trying to validate id: {e}")

def validate_customers(df):
    try:
        validation_results = pd.DataFrame(index=df.index) #make a DataFrame for validation results
        validation_results["missing_customer_id"] = ~check_for_null(df, column = "customer_id")
        validation_results["duplicate_customer_id"] = ~validate_duplicates(df, column='customer_id')
        validation_results["missing_customer_name"] = ~check_for_null(df, column="name")
        validation_results["missing_email"] = ~check_for_null(df, column="email")
        validation_results["invalid_email"] = ~validate_email(df)
        validation_results["missing_country"] = ~check_for_null(df, column="country")
        validation_results["missing_date"]= ~check_for_null(df, column="created_at")
        validation_results["invalid_date"] = ~validate_date(df, column ="created_at")
        validation_results["is_valid"] = ~validation_results.any(axis=1)
        return validation_results
    except Exception as e:
        logger.exception(f" There was a problem when trying to validate customers: {e}")

def validate_products(df):
    try:
        validation_results = pd.DataFrame(index = df.index)
        validation_results["missing_product_id"] = ~check_for_null(df, column="product_id")
        validation_results["duplicate_product_id"] = ~validate_duplicates(df, column="product_id")
        validation_results["missing_product_name"] = ~check_for_null(df, column="name")
        validation_results["missing_category"]=~check_for_null(df, column="category")
        validation_results["missing_price"]= ~check_for_null(df, column="price")
        validation_results["invalid_price"] = ~validate_positives(df, column="price")
        validation_results["is_valid"] = ~validation_results.any(axis=1)
        return validation_results
    except Exception as e:
        logger.exception(f" There was a problem when trying to validate products: {e}")

def validate_orders(df, df_existing1, df_existing2):
    try:
        validation_results = pd.DataFrame(index = df.index)
        validation_results["missing_order_id"] = ~check_for_null(df, column="order_id")
        validation_results["missing_customer_id"]= ~check_for_null(df, column="customer_id")
        validation_results["customer_does_not_exist"] = ~id_existing(df_existing1, df, column="customer_id")
        validation_results["missing_product_id"]= ~check_for_null(df, column="product_id")
        validation_results["product_does_not_exist"]= ~id_existing(df_existing2, df, column="product_id")
        validation_results["missing_quantity"]= ~check_for_null(df, column ="quantity")
        validation_results["invalid_quantity"] = ~validate_positives(df, column="quantity")
        validation_results["missing_order_date"]= ~check_for_null(df, column="order_date")
        validation_results["invalid_order_date"]= ~validate_date(df, column = "order_date")

        validation_results["is_valid"] = ~validation_results.any(axis=1)
        return validation_results
    except Exception as e:
        logger.exception(f"There was a problem when trying to validate orders: {e}")

