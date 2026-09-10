#za loadanje v bazo
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

#setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_to_sql(df, table_name):
    #getting env variables for the database where I want to load into
    try:
        load_dotenv()
        db_user = os.getenv('USER')
        db_password = os.getenv('PASSWORD')
        db_host = os.getenv('HOST')
        db_port = os.getenv('PORT')
        db_database = os.getenv('DATABASE')

        #Creating the SQLAlchemy engine
        # The format is: mysql+pymysql://user:password@host:port/database
        engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}')

        # Writes df into the database
        df.to_sql(name = f"{table_name}", con=engine, if_exists ='replace', index=False )
        logger.info(f'Table {table_name} successfully loaded into the database {db_database} as {table_name}')
    except Exception as e:
        logger.exception(f"Something went wrong when loading the table into the database: {e}")
