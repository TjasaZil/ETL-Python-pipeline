
import logging

import pandas as pd
from sqlalchemy import create_engine

from src.paths import SOURCE_DB

logger = logging.getLogger(__name__)

ALLOWED_TABLES = {"customers", "products", "orders"}


def extract_data(table_name: str) -> pd.DataFrame:
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Unsupported table: {table_name}")

    engine = create_engine(
        f"sqlite:///{SOURCE_DB.as_posix()}"
    )

    try:
        df = pd.read_sql_query(
            f'SELECT * FROM "{table_name}"',
            con=engine,
        )

        logger.info(
            "Extracted %s rows from %s",
            len(df),
            table_name,
        )

        return df

    except Exception:
        logger.exception(
            "Error extracting table %s from SQLite",
            table_name,
        )
        raise

    finally:
        engine.dispose()
