# ETL Python Pipeline

A Python-based ETL pipeline for extracting data from CSV files, transforming and validating the data and loading clean records into a MySQL database.

The project is designed as a small-scale data engineering project that demonstrates fundamental ETL concepts, data quality checks, error handling, logging and SQL-based data storage.

## Project overview

The pipeline processes three datasets:

- Customers - customer information
- Products - product information
- Orders - customer orders and purchased products

Each dataset goes through its own ETL pipeline.
The goal is to ensure that only valid and cleaned data is loaded into the database, while invalid records are removed and perserved separately.

## Technologies:

- Python
- Pandas
- MySQL
- SQLAlchemy
- PyMySQL
- Python-dotenv
- Git / GitHub
- Logging

## Project structure

```
ETL-Python-pipeline/
|
|-- .github/
|  |-- workflows/
|  |  |-- allow-merge-to-main.yml
|  |  |-- auto-pr.yml
| 
|-- data/
|  |-- customers.csv
|  |-- orders.csv
|  |-- products.csv
|
|-- output/
|  |-- invalid/
|  |  |-- customers_invalid.csv
|  |  |-- orders_invalid.csv
|  |  |-- products_invalid.csv
|  |-- reports/
|  |  |-- customres_report.json
|  |  |-- orders_report.json
|  |  |-- products_report.json
|
|-- sql_analysis/
|  |-- example.sql
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
|  |-- country_codes.py
|  |-- main.py
|
|-- .env.example
|-- .gitignore
|-- README.md

```

## ETL Process

### Extract

The extraction step reads the source CSV files using Pandas.</br>
The files from where we are extracting the data are in the `data/` folder

### Validate

Before transformation, the data is validated against rules, specific to each dataset.

**Customers:**

- `customer_id` must not be NULL
- `name` must not be NULL
- `email` must not be NULL
- `email` must have a valid format
- `country` must not be NULL
- `created_at` must be a valid date
- `records` should not be duplicated

**Products:**

- `product_id` must not be NULL
- `name` must not be NULL
- `category` must not be NULL
- `quantity` must be greater than 0
- `order_date` must be valid date
- `records` should not be duplicated

**Orders:**

- `order_id` must not be NULL
- `customer_id` must not be null
- `product_id` must not be null
- `quantity` must be greater than 0
- `order_date` must be valid

Validation is performed independently for each rule so that a single record san have multiple validation errors (this is done for more extensive reporting)

### Invalid data handling

Invalid records are not just deleted.<br>
Each dataset has it's own invalid output `.cvs` file, that is generated in the `output/invalid` folder and each record contains a `rejection_reason` column, where it is described why the row was rejected

#### Validation statistics 

The pipeline also generates validation statistic for each dataset. <br>
The report distinguishes between:

- **input rows** - total number of records read from the source file
- **valid rows** - records that passed all validation rules
- **rejected rows** - unique records that failed at least one validation rule
- **validation failures** - number of times individual rules were violated

**Example of validation statistics:**

```
{
    "input rows": 1014,
    "valid rows": 672,
    "rejected rows": 342,
    "validation failures": {
        "missing_values": 115,
        "invalid_email": 25,
        "invalid_date": 248,
        "duplicate_customer_id": 48
    }
}
```

A row can fail multiple validation rules. For instance one record can have a missing name, invalid email and invalid date. A record like that is counted once as rejected, but contributes to all three individual validation failure counters. <br>
This prevents rejected records from being counted more than once.

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

### Loading

After the transformation and validation, only valid records are loaded into a MySQL database. <br>
Each dataset is loaded into a separate table, with a name corresponding to the dataset name.
Loaded data can then be queried using SQL.

### SQL Analysis

We can do some analysis using the cleaned and transformed data from the dataset.
Here are some of the questions that we can explore, using different queries:

- Top 10 most ordered products of all time.
- Which customers have placed the most orders?
- What is the total quantity sold for each product?
- What is the total revenue by product category?
- Which customers generated the highest revenue?
- How many orders were placed each day?
- Which products have never been ordered?
- Which month were the most customers 'created'?
- Which countries are most customers from?

Example queries are written in the `sql_analysis/` folder

## Configuration
Database credentials are stored in environment variables rather than directly in the source code.<br>
This is an example of the `.env` file:
```dotenv
USER='your_username'
PASSWORD='your_password'
HOST='localhost'
PORT=3306
DATABASE='your_database'
```
Personal `.env` file is excluded from Git, using `.gitignore.`<br>
An `.env.example` file is included in the repository to show the required configuration without exposing credentials.

## Installation 
Prerequisites:
- MySQL installed 
- Python installed
- Git installed

Clone the repository and open it with your code editor of choice.
```
https://github.com/TjasaZil/ETL-Python-pipeline.git
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
pip install -r requirements.txt
```
Rename `.env.example` file into `.env` and write in your MySQL credentials.<br>

Run the pipelines
```
python -m src.main
```

There are three individual pipelines, one for each dataset. The pipeline extracts data from the `.csv` file, validates it against specific rules and removes invalid rows into it's own `.csv` files.
Valid data is then transformed and loaded into MySQL database.<br>
After the execution of the pipelines the database should be populated with tables and there should be an `output/` folder in the repository.<br>
Invalid data are stored in `output/invalid/` folder and simple reports are generated in the `output/reports/` folder.

## Future improvements:

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
- Loading data into MySQL
- Using Git and GitHub
- Documenting a data pipeline
