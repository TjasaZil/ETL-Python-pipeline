# za generiranje reportov
import json
import logging

from sqlalchemy import create_engine, text

from src.paths import QUALITY_DB

logger = logging.getLogger(__name__)

# adds rejection reasons to each row (why the data will be removed after validation)
# this function takes the original data and it's validation results and returns only invalid rows with added reasons for rejection
def add_rejection_reasons(df, validation_results):
    try:
        #identify rejection reasons for every row
        invalid_df = df[~validation_results["is_valid"]].copy() #taking only rows where is_valid is false -> those are the rows where we have at least one validation problem
        invalid_df["rejection_reasons"] = "" #add a rejection reasons column to put all of the reasons into one column
        for index, row in invalid_df.iterrows():
            validation_row = validation_results.loc[index]
            reasons = validation_row[validation_row].index.tolist() # validation_row[validation_columns][validation_row[validation_columns]].index.tolist()
            invalid_df.loc[index, "rejection_reasons"] = ", ".join(reasons)
        return invalid_df
    except Exception as e:
        logger.exception(f"Problems with adding rejection reasons: {e}")


#this function saves the invalid data into it's own file

def save_invalid_data(df, table_name):
    engine = create_engine(
        f"sqlite:///{QUALITY_DB.as_posix()}"
    )

    try:
        with engine.begin() as connection:
            df.to_sql(
                name=f"{table_name}_invalid",
                con=connection,
                if_exists="append",
                index=False,
            )

        logger.info(
            "Saved %s invalid rows for %s",
            len(df),
            table_name,
        )

    except Exception:
        logger.exception("Failed to save invalid records")
        raise

    finally:
        engine.dispose()


#creates a python dictionary from the invalid data
def create_report(df, validation_results, dataset_name):
    try:
        input_rows = len(df) #this is all of the rows in the dataset
        valid_rows = int((validation_results["is_valid"]).sum()) #all rows without any errors
        rejected_rows = int((~validation_results["is_valid"]).sum()) #all rows with at least one invalid data
        validation_failures={}
        for column in validation_results.columns:
            if column == 'is_valid':
                continue
            validation_failures[column] = int(validation_results[column].sum()) #counts validation errors
        report={
            "dataset": dataset_name,
            "input_rows": input_rows,
            "valid_rows": valid_rows,
            "rejected_rows": rejected_rows,
            "validation_failures": validation_failures
        }
        return report
    except Exception as e:
        logger.exception(f"Problems with creating report: {e}")

#changes the data dictionary into a json format and saves it
def save_report(report, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=4)
        logger.info(f"Successfully saved {filepath}")
    except Exception as e:
        logger.exception(f"Problems with saving report:{e}")


def save_report_to_sqlite(report):
    engine = create_engine(
        f"sqlite:///{QUALITY_DB.as_posix()}"
    )

    try:
        with engine.begin() as connection:
            connection.execute(
                text("""
                    CREATE TABLE IF NOT EXISTS validation_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        dataset TEXT NOT NULL,
                        report_json TEXT NOT NULL
                    )
                """)
            )

            connection.execute(
                text("""
                    INSERT INTO validation_reports (
                        dataset,
                        report_json
                    )
                    VALUES (
                        :dataset,
                        :report_json
                    )
                """),
                {
                    "dataset": report["dataset"],
                    "report_json": json.dumps(
                        report,
                        ensure_ascii=False,
                    ),
                },
            )

        logger.info(
            "Saved validation report for %s",
            report["dataset"],
        )

    except Exception:
        logger.exception("Failed to save report to SQLite")
        raise

    finally:
        engine.dispose()