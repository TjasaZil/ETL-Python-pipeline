#ETL pipeline for customers.csv
from src.functions.extract import extract_data
from src.functions.validate import validate_customers
from src.functions.report import add_rejection_reasons, save_invalid_data, create_report, save_report
from src.functions.transform import transform_customers
from src.functions.load import load_to_sql

customers_invalid_path ="/output/invalid/customers_invalid.csv"
customers_report_path ="/output/reports/customers_report.json"

def customers_pipeline(file_path):
    #extract data
    customers_df = extract_data(file_path)
    #validate data
    validated_customer_results = validate_customers(customers_df)
    #get invalid data and save it into it's own file
    invalid_customer_data = add_rejection_reasons(customers_df, validated_customer_results)
    save_invalid_data(invalid_customer_data, customers_invalid_path)
    #report invalid data -> make a report and save it
    customer_report = create_report(customers_df, validated_customer_results)
    save_report(customer_report, customers_report_path)
    #transform valid data
    valid_customer_df = customers_df[validated_customer_results["is_valid"]].copy()
    #Load into database
    ready_for_db= transform_customers(valid_customer_df)
    load_to_sql(ready_for_db, table_name="customers")
