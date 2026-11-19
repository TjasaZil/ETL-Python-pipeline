from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
REPORT_DIR = OUTPUT_DIR / "reports"
DATABASE_DIR = BASE_DIR / "databases"
SRC_DIR = BASE_DIR / "src"

for directory in (
    REPORT_DIR,
    DATABASE_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

# SQLite databases
SOURCE_DB = DATABASE_DIR / "source.db"
QUALITY_DB = DATABASE_DIR / "quality.db"
ANALYTICS_DB = DATABASE_DIR / "analytics.db"


# JSON validation reports
customers_report_path = REPORT_DIR / "customers_report.json"
orders_report_path = REPORT_DIR / "orders_report.json"
products_report_path = REPORT_DIR / "products_report.json"
