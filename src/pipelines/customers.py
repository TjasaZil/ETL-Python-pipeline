#ETL pipeline for customers.csv

from src.functions.extract import extract_data
from src.functions.transform import transform_customers
from src.functions.validate import validate_customers
from src.functions.report import (
    add_rejection_reasons,
    save_invalid_data,
    create_report,
    save_report,
    save_report_to_sqlite,
)
from src.functions.load import load_valid_data


def customers_pipeline():
    # Extract
    customers_df = extract_data("customers")

    # Transform
    transformed_df = transform_customers(
        customers_df.copy()
    )

    # Validate
    validated_df = validate_customers(transformed_df)

    if validated_df is None:
        raise RuntimeError("Customer validation failed")

    # Invalid records
    invalid_df = add_rejection_reasons(
        customers_df,
        validated_df,
    )

    save_invalid_data(invalid_df, "customers")

    # Report
    report = create_report(
        customers_df,
        validated_df,
        dataset_name="customers",
    )

    save_report(report, "output/reports/customers_report.json")
    save_report_to_sqlite(report)

    # Valid records
    ready_for_db = transformed_df.loc[
        validated_df["is_valid"]
    ].copy()

    load_valid_data(ready_for_db, "customers")

    return ready_for_db

