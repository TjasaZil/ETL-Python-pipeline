#ETL pipeline for orders.csv

from src.functions.extract import extract_data
from src.functions.transform import transform_orders
from src.functions.validate import validate_orders
from src.functions.report import (
    add_rejection_reasons,
    save_invalid_data,
    create_report,
    save_report,
    save_report_to_sqlite,
)
from src.functions.load import load_valid_data
from src.paths import orders_report_path


def orders_pipeline(df_customers, df_products):
    orders_df = extract_data("orders")

    transformed_df = transform_orders(
        orders_df.copy()
    )

    validated_df = validate_orders(
        transformed_df,
        df_customers,
        df_products,
    )

    if validated_df is None:
        raise RuntimeError("Order validation failed")

    invalid_df = add_rejection_reasons(
        orders_df,
        validated_df,
    )

    save_invalid_data(invalid_df, "orders")

    report = create_report(
        orders_df,
        validated_df,
        dataset_name="orders",
    )

    save_report(report, orders_report_path)
    save_report_to_sqlite(report)

    ready_for_db = transformed_df.loc[
        validated_df["is_valid"]
    ].copy()

    load_valid_data(ready_for_db, "orders")

    return ready_for_db
