#ETL pipeline for customers.csv
from src.functions.extract import extract_data
from src.functions.validate import validate_customers
from src.functions.report import add_rejection_reasons, save_invalid_data, create_report, save_report
from src.functions.transform import transform_customers
from src.functions.load import load_to_sql
from src.paths import customers_invalid_path, customers_report_path



def customers_pipeline(file_path):
    #extract data
    customers_df = extract_data(file_path)

    #transform data
    transformed_df = transform_customers(customers_df)

    #validate data
    validated_df = validate_customers(transformed_df)

    #get invalid data and generate a report
    invalid_df = add_rejection_reasons(customers_df, validated_df)
    save_invalid_data(invalid_df, customers_invalid_path)

    report_df = create_report(customers_df, validated_df)
    save_report(report_df, customers_report_path)

    #Load into database
    ready_for_db = transformed_df[validated_df["is_valid"]].copy()
    #print(ready_for_db)
    load_to_sql(ready_for_db, table_name="customers")
