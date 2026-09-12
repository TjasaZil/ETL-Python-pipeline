#ETL pipeline for orders.csv
from src.functions.extract import extract_data
from src.functions.validate import validate_orders
from src.functions.report import add_rejection_reasons, save_invalid_data, create_report, save_report
from src.functions.transform import transform_orders
from src.functions.load import load_to_sql
from src.paths import orders_invalid_path, orders_report_path

def orders_pipeline(file_path):
    #extract data
    orders_df = extract_data(file_path)

    #Transform data
    transformed_df = transform_orders(orders_df)

    #validate data
    validated_df = validate_orders(transformed_df)

    #get invalid data and generate a report
    invalid_df = add_rejection_reasons(orders_df, validated_df)
    save_invalid_data(invalid_df, orders_report_path)

    report_df = create_report(orders_df, validated_df)
    save_report(report_df, orders_report_path)

    #Load into database
    ready_for_db = transformed_df[validated_df["is_valid"]].copy()
    #print(ready_for_db)
    #load_to_sql(ready_for_db, table_name="orders")