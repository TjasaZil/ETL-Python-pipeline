# ETL Python Pipeline

A Python-based ETL pipeline for extracting data from SQLite, transforming and validating the data and loading clean 
records into a SQLite database.

The project is designed as a small-scale data engineering project that demonstrates fundamental ETL concepts, 
data quality checks, error handling, logging and SQL-based data storage.

## Project overview

The pipeline processes three datasets:

- Customers - customer information
- Products - product information
- Orders - customer orders and purchased products

Each dataset goes through its own ETL pipeline.
The goal is to ensure that only valid and cleaned data is loaded into the database, while invalid records are 
removed and preserved separately.

This project uses three SQLite databases:
- source.db: Stores the original data
- analytics.db: Stores transformed and validated records for analysis
- quality.db: Stores rejected records and validation reports

JSON validation reports are also generated in the `output/reports/` directory.

## Technologies:

- Python
- Pandas
- SQLite
- SQLAlchemy
- Git / GitHub
- Logging
- pathlib

## Project structure

```
ETL-Python-pipeline/
|
|-- .github/
|  |-- workflows/
|  |  |-- allow-merge-to-main.yml
|  |  |-- auto-pr.yml
| 
|-- databases/
|  |-- analytics.db
|  |-- quality.db
|  |-- source.db
|
|-- output/
|  |-- reports/
|  |  |-- customers_report.json
|  |  |-- orders_report.json
|  |  |-- products_report.json
|
|-- sql_analysis/
|  |-- queries.sql
|
|-- src/
|  |-- functions/
|  |  |-- extract.py
|  |  |-- load.py
|  |  |-- report.py
|  |  |-- transform.py
|  |  |-- validate.py
|  |-- pipelines/
|  |  |-- customers.py
|  |  |-- orders.py
|  |  |-- products.py
|  |-- scripts/
|  |  |-- ingest.py
|  |-- country_codes.py
|  |-- main.py
|  |-- paths.py
|
|-- .gitattributes
|-- .gitignore
|-- README.md
|-- requirements.txt

```
***Note: SQLite database files are created locally when the corresponding scripts run. 
The exact repository structure may differ slightly depending on which files are committed to Git.***

## ETL Process

### Ingestion
***(This step was already done in advance. there are no csv files in this repo from which user can ingest from. 
All of the data is in the `.db` files).***

The initial ingestion step imports the three source CSV files from the `data/` directory into SQLite.

The `src/scripts/ingest.py` script reads the CSV files using Pandas and writes their contents into the corresponding tables in source.db:

- customers
- products
- orders

This is a separate step from the main ETL pipeline. After ingestion, 
the ETL pipelines extract data from SQLite rather than reading the CSV files directly.

### Extract

The extraction stage reads data from `source.db` using Pandas and SQLAlchemy.

Each dataset is extracted independently using the reusable `extract_data()` function. Only explicitly 
allowed table names can be queried.

### Transform

The transformation stage cleans and standardizes the raw data after validation. Examples of transformations include: <br>

- removing leading and trailing whitespace
- normalizing multiple spaces
- standardizing names using 'Title Case'
- converting emails to lowercase
- converting country names to country codes
- converting date strings into proper date values
- converting numeric columns into appropriate numeric types

Example transformations:

1. Removing leading and trailing whitespace, normalizing multiple spaces, standardizing names using Title Case

```
"JOhN   SmiTh  "
      |
      v
 "John Smith"
```

2. converting date strings into proper date values

```
"27/07/2026"
     |
     v
2026-07-27
```

Dates are converted into proper date values, so that they can be stored in the database using an appropriate DATE column.

### Validate

After transformation, the data is validated against rules, specific to each dataset.

**Customers:**

- `customer_id` must not be NULL
- `customer_id` must me unique
- `name` must not be NULL
- `email` must not be NULL
- `email` must have a valid format
- `country` must not be NULL
- `created_at` must not be NULL
- `created_at` must be a valid date

**Products:**

- `product_id` must not be NULL
- `product_id` must be a numeric value
- `product_id` must not be duplicated
- `name` must not be NULL
- `category` must not be NULL
- `price` must be a numeric value
- `price` must not be NULL
- `price` must be greater than 0
- 
**Orders:**

- `order_id` must not be NULL
- `order_id` must be a numeric value
- `customer_id` must not be null
- `customer_id` must be a numeric value
- `customer_id` must exist in the 'customer' table
- `product_id` must not be null
- `product_id` must be a numeric value
- `product_id` must exist in the 'products' table
- `quantity` must not be NULL
- `quantity` must be greater than 0
- `quantity` must be a numeric value
- `order_date` must not be NULL
- `order_date` must be valid

Validation is performed independently for each rule so that a single record can have multiple validation errors (this is done for more extensive reporting)

### Invalid data handling

Invalid records are not simply discarded. They are preserved in the `quality.db` database in separate tables:

- customers_invalid
- products_invalid
- orders_invalid

Each rejected record includes a `rejection_reasons` field describing the validation rules it failed.

This makes it possible to investigate data quality issues without contaminating the analytics database.

#### Validation statistics 

For each dataset, the pipeline generates a JSON report in `output/reports/.` </br>
Validation reports are also stored in `quality.db.` </br>

- **input rows** - total number of records read from the source file
- **valid rows** - records that passed all validation rules
- **rejected rows** - unique records that failed at least one validation rule
- **validation failures** - number of times individual rules were violated

**Example of validation statistics:**

```
{
    "input rows": 1014,
    "valid rows": 652,
    "rejected rows": 362,
    "validation failures": {
        "missing_customer_id": 22,
        "duplicate_customer_id": 48,
        "missing_customer_name": 35,
        "missing_email": 15,
        "invalid_email": 25,
        "missing_country_": 53,
        "missing_date": 30,
        "invalid_date": 246
    }
}
```

A row can fail multiple validation rules. For instance one record can have a missing name, invalid email and invalid date. A record like that is counted once as rejected, but contributes to all three individual validation failure counters. <br>
This prevents rejected records from being counted more than once.

### Loading

Valid records are loaded into `analytics.db` using SQLAlchemy and Pandas.

The database contains three tables:
- customers
- products
- orders

The pipeline uses SQLite, so no separate database server or MySQL Workbench installation is required.

The analytics database is kept separate from the source and data quality databases, allowing analytical 
queries to operate on cleaned records while preserving rejected records for investigation.

Note: The current loading implementation uses append-based inserts. Repeated runs may duplicate data or 
encounter uniqueness conflicts unless the tables are reset or an appropriate upsert strategy is implemented.

### SQL Analysis

The cleaned data in `analytics.db` can be queried using SQL.
Example analytical questions include:

- Top 10 most ordered products of all time.
- Which customers have placed the most orders?
- What is the total quantity sold for each product?
- What is the total revenue by product category?
- Which customers generated the highest revenue?
- How many orders were placed each day?
- Which products have never been ordered?
- Which month were the most customers 'created'?
- Which countries are most customers from?

Example queries are written in the `sql/queries.sql` file

## Installation 
Prerequisites:
- Python 3.10 or later recommended 
- Git 
- A SQLite-compatible database viewer (optional)

SQLite is included with standard Python installations, so a separate database server is not required.

Clone the repository and open it with your code editor of choice.
```
git clone https://github.com/TjasaZil/ETL-Python-pipeline.git
cd ETL-Python-pipeline
```
Create a virtual environment
```
python -m venv venv
```
Activate it
- Windows
```
venv\Scripts\activate
```
- Linux / macOS
```
source venv/bin/activate
```
Install dependencies
```
python -m install -r requirements.txt
```

Run the ETL pipeline
```
python -m src.main
```

The main pipeline:

Extracts customers, products, and orders from `source.db`.
Transforms and validates each dataset.
Stores invalid records and validation reports in `quality.db`.
Generates JSON validation reports in `output/reports/`.
Loads valid records into `analytics.db`.
The pipeline logs the number of extracted, rejected, and loaded records.

Inspect the results:

Open the following files with a SQLite-compatible database viewer:

- `databases/source.db`
- `databases/analytics.db`
- `databases/quality.db`

You can also inspect the JSON reports in `output/reports/`.


## Future improvements:

- [x] **migrate input data from .csv to sqlite .db** - *[added on 19.11.2026 - pipeline for auto-pr to `development` branch]*
- [x] **migrate output data from .csv and .json to sqlite .db** - *[added on 19.11.2026 - pipeline for auto-pr to `development` branch]*
- [ ] migrate from workbench to sqlite .db
- [ ] containerizing the application with Docker
- [ ] adding a Docker Compose setup for MySQL
- [x] **adding a CI/CD pipeline with GitHub Actions** - *[added on 11.09.2026 - pipeline for auto-pr to `development` branch]*
- [ ] adding tests using pytest
- [ ] improving pipeline configuration
- [ ] adding database schema migrations
- [ ] adding pipeline execution metrics
- [ ] scheduling the pipeline
- [ ] adding monitoring and alerting
- [x] **restrict `master` branch** - *[added on 11.09.2026 - `master` branch requires PR before merge]*

## What this project demonstrates:

This project was built to demonstrate practical understanding of several fundamental data engineering concepts:

- Building an ETL pipeline in python
- Working with structured data using pandas
- Data cleaning and transformation
- Data validation and simple quality checks
- Handling invalid data
- Designing reusable pipeline components
- Working with relational databases
- Loading data into SQLite
- Using Git and GitHub
- Documenting a data pipeline
