from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
INVALID_DIR = OUTPUT_DIR / "invalid"
REPORT_DIR = OUTPUT_DIR / "reports"
DATABASE_DIR = BASE_DIR / "databases"
SRC_DIR = BASE_DIR / "src"

for directory in (
    INVALID_DIR,
    REPORT_DIR,
    DATABASE_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

# CSV input files
customers_path = DATA_DIR / "customers.csv"
orders_path = DATA_DIR / "orders.csv"
products_path = DATA_DIR / "products.csv"

# SQLite databases
SOURCE_DB = DATABASE_DIR / "source.db"
QUALITY_DB = DATABASE_DIR / "quality.db"
ANALYTICS_DB = DATABASE_DIR / "analytics.db"

# Optional legacy CSV outputs during migration
customers_invalid_path = INVALID_DIR / "customers_invalid.csv"
orders_invalid_path = INVALID_DIR / "orders_invalid.csv"
products_invalid_path = INVALID_DIR / "products_invalid.csv"

# JSON validation reports
customers_report_path = REPORT_DIR / "customers_report.json"
orders_report_path = REPORT_DIR / "orders_report.json"
products_report_path = REPORT_DIR / "products_report.json"
