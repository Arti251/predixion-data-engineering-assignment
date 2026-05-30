import sqlite3
import pandas as pd
from datetime import datetime


def main():

    # Read transformed data
    df = pd.read_csv("data/transformed_calls.csv")

    # Connect to SQLite
    conn = sqlite3.connect("call_data.db")

    # Load calls table
    df.to_sql(
        "calls",
        conn,
        if_exists="replace",
        index=False
    )

    # Create ingestion log
    ingestion_log = pd.DataFrame([
        {
            "run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "records_processed": len(df),
            "rejected_count": len(pd.read_csv("data/rejected_log.csv"))
        }
    ])

    ingestion_log.to_sql(
        "ingestion_log",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("\nLOAD COMPLETE")
    print("-" * 40)
    print(f"Records loaded: {len(df)}")
    print("Database: call_data.db")
    print("Tables created:")
    print("- calls")
    print("- ingestion_log")


if __name__ == "__main__":
    main()