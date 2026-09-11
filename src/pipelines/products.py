#ETL pipeline for products.csv
from src.functions.extract import extract_data
from src.functions.validate import validate_products
from src.functions.report import add_rejection_reasons, save_invalid_data, create_report, save_report
from src.functions.transform import transform_products
from src.functions.load import load_to_sql

products_invalid_path ="output/invalid/products_invalid.csv"
products_report_path ="output/reports/products_report.json"

def products_pipeline(file_path):
    #extract data
    products_df = extract_data(file_path)
    #validate data
    validated_products_results = validate_products(products_df)
    #get invalid data and save it into it's own file
    invalid_products_data = add_rejection_reasons(products_df, validated_products_results)
    save_invalid_data(invalid_products_data, products_invalid_path)
    #report invalid data -> make a report and save it
    products_report = create_report(products_df, validated_products_results)
    save_report(products_report, products_report_path)
    #transform valid data
    valid_products_df = products_df[validated_products_results["is_valid"]].copy()
    ready_for_db = transform_products(valid_products_df)
    load_to_sql(ready_for_db, table_name="products")