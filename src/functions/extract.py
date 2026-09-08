import pandas as pd
import logging

#setup logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 1. extracting data

#customers_df = pd.read_csv("../data/customers.csv")
#orders_df = pd.read_csv("../data/orders.csv")
#products_df = pd.read_csv("../data/products.csv")

def extract_data(file_path):
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Extracting data from {file_path} was successful")
        return df
    except Exception as e:
        logger.info(f"Extracting data from {file_path} was failed")
        logger.error(e)
        raise