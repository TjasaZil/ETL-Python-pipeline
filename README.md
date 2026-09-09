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
- Git / GitHub
- Logging

## Project structure

```
ETL-Python-pipeline/
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
|  |  |-- pipeline_report.json
|  |  |-- products_report.json
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
|-- .gitignore
|-- README.md

```

## ETL Process

### Extract

The extraction step reads the source CSV files using Pandas.</br>
The pipeline heeps extraction separate from validation and transformation, so that each stage has clear responsibility.</br>
The files from where we are extracting the data are in the `data/` folder

### Transform

The transformation stage cleans and standardizes the raw data before validation. Examples of transformations include: <br>

- removing leading and trailing whitespace
- normalizing muiltiple spaces
- standardizing names using 'Title Case'
- converting emails to lowercase [DO IT - Because mails are not case sensitive]
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
- `name` must not be NULL
- `email` must not be NULL
- `email` must have a valid format
- `country` must not be NULL
- `country` must be valid [DO IT]
- `created_at` must be a valid date
- `records` should not be duplicated

**Products:**

- `product_id` must not be NULL
- `name must` not be NULL
- `category` must not be NULL
- `quantity` must be greater than 0
- `order_date` must be valid date
- `referenced` customer and product IDs must exist [NOT IMPLEMENTED]
- `records` should not be duplicated

**Orders:**

- `order_id` must not be NULL
- `customer_id` must not be null
- `product_id` must not be null
- `quantity` must be greater than 0
- `order_date` must be valid

Validation is performed independently for each rule so that a single record san have multiple validation errors (this is done for more extensive reporting)

### Invalid data handling [TO IMPLEMENT]

Invalid records are not just deleted.<br>
Each dataset has it's own invalid output `.cvs` file, that is generated in the `output/invalid` folder and each record contains a `rejection_reason` column, where it is described why the row was rejected

#### Validation statistics [TO IMPLEMENT]

The pipeline also generates validation statistic for each dataset. <br>
The report distinguishes between:

- **input rows** - total number of records read from the source file
- **valid rows** - records that passed all validation rules
- **rejected rows** - unique records that failed at least one validation rule
- **loaded rows** - records successfully loaded into MySQL
- **validation failures** - number of times individual rules were violated

**Example of validation statistics:**

```
[DO EXAMPLE]
```

A row can fail multiple validation rules. For instance one record can have a missing name, invalid email and invalid date. A record like that is counted once as rejected, but contributes to all three individual validation failure counters. <br>
This prevents rejected records from being counted more than once.

#### Data Reconciliation [TO IMPLEMENT]

The pipeline performs basic reconciliation checks after validation and loading. <br><br>
It is expected that the number of **input rows** is the same as the number of **valid** and **invalid rows** combined (total number of records, read from the source file, must be the same as the sum of records that passed all validation checks, and unique records that failed at least one validation rule). And the number of **valid rows** must be the same as the number of **loaded rows** (number of rows that passed all validation rules is the same as number of rows loaded into MySQL).<br><br>
If these numbers do not match, the pipeline reports an error, which helps detect unexpected data loss during processing.

### Loading [TO IMPLEMENT]

After the transformation and validation, only valid records are loaded into a MySQL database. <br>
Each dataset is loaded into a separate table, with a name corresponding to the dataset name.
Loaded data can then be queried using SQL.

### SQL Analysis [TO IMPLEMENT]

We can do some analysis using the cleaned and transformed data from the dataset.
Here are some of the questions that we can explore, using different queries:

- Which products have been ordered the most?=
- Which customers have placed the most orders?
- What is the total quantity sold for each product?
- What is the total revenue by product category
- Which customers generated the highest revenue
- How many orders were placed each day?
- Which products have never been ordered?

## Configuration [TO IMPLEMENT]

## Installation [TO IMPLEMENT]

## Future improvements:

- [ ] containerizing the application with Docker
- [ ] adding a Docker Compose setup for MySQL
- [ ] adding a CI/CD pipeline with GitHub Actions
- [ ] adding tests using pytest
- [ ] improving pipeline configuration
- [ ] adding database schema migrations
- [ ] adding pipeline execution metrics
- [ ] scheduling the pipeline
- [ ] adding monitoring and alerting

## What this project demonstrates:

This project was built to demonstrate practical understanding of several fundamental data engineering concepts:

- Building an ETL pipeline in python
- Working with structured data using Pandas
- Data cleaning and transformation
- Data validation and quality checks
- Handling invalid data
- Designing reusable pipeline components
- Working with relational databases
- Loading data into MySQL
- Using Git and GitHub
- Documenting a data pipeline
