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
        counter = 0
        header = df.head(1)
        print(header)
        with open(f"../data/invalid_data/invalid_null.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for index, row in df.iterrows():
                if row.isnull().values.any():
                    counter += 1
                    writer.writerow(row.values)
                    df.dropna(inplace=True)
        logger.info(f"Checked for null values and removed them from the dataframe. There were {counter} rows removed")
        return df
    except Exception as e:
        logger.error(f" There was a problem when checking for null values: {e}")


#validating email
def validate_email(df):
    try:
        counter = 0
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        header = df.head(1)
        print(header)
        with open(f"../data/invalid_data/invalid_email.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for index, email in df["email"].items():
                if not re.match(pattern, str(email)):
                    counter += 1
                    row = df.loc[index]
                    writer.writerow(row.values)
                    df.drop(index, inplace=True)
        logger.info(f"Checked for valid emails and removed invalid emails from the dataframe. There were {counter} rows removed")
        return df
    except Exception as e:
        logger.error(f" There was a problem when trying to validate email: {e}")

#validating that the date is not in the future
def validate_date(df):
    standardized_date=standardize_date_format(df)
    try:
        current_date = pd.Timestamp.today()
        counter = 0
        header = df.head(1)
        print(header)
        with open("../data/invalid_data/invalid_date.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for col in standardized_date.columns:
                if col == 'created_at' or col == 'order_date':
                    for index, value in standardized_date[col].items():
                        if value > current_date:
                            counter += 1
                            row = df.loc[index]
                            writer.writerow(row.values)
                            df.drop(index, inplace=True)
                    logger.info(
                        f"Checked for valid date and removed invalid dates from the dataframe. There were {counter} rows removed")
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