
import logging

import pandas as pd
from sqlalchemy import create_engine

from src.paths import ANALYTICS_DB, QUALITY_DB

logger = logging.getLogger(__name__)

ALLOWED_TABLES = {"customers", "products", "orders"}


def load_to_sqlite(
    df: pd.DataFrame,
    table_name: str,
    database_path,
):
    if table_name not in ALLOWED_TABLES and not table_name.endswith("_invalid"):
        raise ValueError(f"Unsupported table: {table_name}")

    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}"
    )

    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
        )

        logger.info(
            "Loaded %s rows into table %s",
            len(df),
            table_name,
        )

    except Exception:
        logger.exception(
            "Failed to load table %s into SQLite",
            table_name,
        )
        raise

    finally:
        engine.dispose()


def load_valid_data(df, table_name):
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Unsupported table: {table_name}")

    load_to_sqlite(
        df,
        table_name,
        ANALYTICS_DB,
    )


def load_invalid_data(df, table_name):
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Unsupported table: {table_name}")

    load_to_sqlite(
        df,
        f"{table_name}_invalid",
        QUALITY_DB,
    )

