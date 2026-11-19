
import logging

import pandas as pd
from sqlalchemy import create_engine

from src.paths import DATA_DIR, SOURCE_DB

logger = logging.getLogger(__name__)

TABLE_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
}


def ingest_csv_to_sqlite():
    engine = create_engine(
        f"sqlite:///{SOURCE_DB.as_posix()}"
    )

    try:
        # Read all CSV files before replacing source tables.
        datasets = {}

        for table_name, filename in TABLE_FILES.items():
            file_path = DATA_DIR / filename

            df = pd.read_csv(
                file_path,
                dtype=str,
                keep_default_na=False,
                skipinitialspace=True,
            )

            # Treat empty strings and whitespace-only values as missing.
            df = df.replace(r"^\s*$", pd.NA, regex=True)

            datasets[table_name] = df

        # Replace all three source tables in one transaction.
        with engine.begin() as connection:
            for table_name, df in datasets.items():
                df.to_sql(
                    name=table_name,
                    con=connection,
                    if_exists="replace",
                    index=False,
                )

                logger.info(
                    "Imported %s rows into %s",
                    len(df),
                    table_name,
                )

    except Exception:
        logger.exception("CSV ingestion failed")
        raise

    finally:
        engine.dispose()


ingest_csv_to_sqlite()