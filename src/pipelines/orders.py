#ETL pipeline for orders.csv
from src.functions.extract import extract_data
from src.functions.validate import validate_orders
from src.functions.report import add_rejection_reasons, save_invalid_data, create_report, save_report
from src.functions.transform import transform_orders
from src.functions.load import load_to_sql

orders_invalid_path ="/output/invalid/orders_invalid.csv"
orders_report_path ="/output/reports/orders_report.json"

def orders_pipeline(file_path):
    #extract data
    orders_df = extract_data(file_path)
    #validate data
    validated_orders_results = validate_orders(orders_df)
    #get invalid data and save it into it's own file
    invalid_orders_data = add_rejection_reasons(orders_df, validated_orders_results)
    save_invalid_data(invalid_orders_data, orders_invalid_path)
    #report invalid data -> make a report and save it
    orders_report = create_report(orders_df, validated_orders_results)
    save_report(orders_report, orders_report_path)
    #transform valid data
    valid_orders_df = orders_df[validated_orders_results["is_valid"]].copy()
    #Load into database
    ready_for_db = transform_orders(valid_orders_df)
    load_to_sql(ready_for_db, table_name="orders")