import pandas as pd
import logging

#setup logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def extract_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        logger.exception(f"There was an error while extracting the data: {e}")
        raise