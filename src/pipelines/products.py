#ETL pipeline for products.csv

from src.functions.extract import extract_data
from src.functions.transform import transform_products
from src.functions.validate import validate_products
from src.functions.report import (
    add_rejection_reasons,
    save_invalid_data,
    create_report,
    save_report,
    save_report_to_sqlite,
)
from src.functions.load import load_valid_data
from src.paths import products_report_path


def products_pipeline():
    products_df = extract_data("products")

    transformed_df = transform_products(
        products_df.copy()
    )

    validated_df = validate_products(transformed_df)

    if validated_df is None:
        raise RuntimeError("Product validation failed")

    invalid_df = add_rejection_reasons(
        products_df,
        validated_df,
    )

    save_invalid_data(invalid_df, "products")

    report = create_report(
        products_df,
        validated_df,
        dataset_name="products",
    )

    save_report(report, products_report_path)
    save_report_to_sqlite(report)

    ready_for_db = transformed_df.loc[
        validated_df["is_valid"]
    ].copy()

    load_valid_data(ready_for_db, "products")

    return ready_for_db
