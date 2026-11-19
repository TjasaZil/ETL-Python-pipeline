# Automating ETL Process wth Python

import logging

from src.pipelines.customers import customers_pipeline
from src.pipelines.products import products_pipeline
from src.pipelines.orders import orders_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting ETL pipeline")

    # Read from source.db, transform, validate and load valid records
    df_customers = customers_pipeline()
    df_products = products_pipeline()
    df_orders = orders_pipeline(df_customers, df_products)

    logger.info(
        "ETL completed. Loaded %s customers, %s products and %s orders.",
        len(df_customers),
        len(df_products),
        len(df_orders),
    )


if __name__ == "__main__":
    main()



