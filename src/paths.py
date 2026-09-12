from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
INVALID_DIR = OUTPUT_DIR / "invalid"
REPORT_DIR = OUTPUT_DIR / "reports"
SRC_DIR = BASE_DIR / "src"
INVALID_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


customers_path= DATA_DIR / "customers.csv"
orders_path= DATA_DIR / "orders.csv"
products_path = DATA_DIR / "products.csv"

products_invalid_path = INVALID_DIR / "products_invalid.csv"
products_report_path =REPORT_DIR /  "products_report.json"
orders_invalid_path = INVALID_DIR /"orders_invalid.csv"
orders_report_path =REPORT_DIR / "orders_report.json"
customers_invalid_path =INVALID_DIR / "customers_invalid.csv"
customers_report_path =REPORT_DIR / "customers_report.json"
