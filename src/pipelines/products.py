#ETL pipeline for products.csv
from src.functions.extract import extract_data
from src.functions.validate import validate_products
from src.functions.report import add_rejection_reasons, save_invalid_data, create_report, save_report
from src.functions.transform import transform_products
from src.functions.load import load_to_sql
from src.paths import products_invalid_path, products_report_path

def products_pipeline(file_path):
    #extract data
    products_df = extract_data(file_path)

    #Transform data
    transformed_df = transform_products(products_df)

    #Validate data
    validated_df = validate_products(transformed_df)

    #get invalid data and generate a report
    invalid_df = add_rejection_reasons(products_df, validated_df)
    save_invalid_data(invalid_df, products_invalid_path)

    report_df = create_report(products_df, validated_df )
    save_report(report_df, products_report_path)

    #load data to MySQL
    ready_for_db = transformed_df[validated_df["is_valid"]].copy()
    #print(ready_for_db)
    #load_to_sql(ready_for_db, table_name="products")