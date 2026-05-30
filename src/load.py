import pandas as pd


def duration_bucket(seconds):
    if seconds < 60:
        return "short"
    elif seconds <= 300:
        return "medium"
    else:
        return "long"


def main():

    df = pd.read_csv("data/valid_records.csv")

    # Convert timestamps
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])

    # Deduplicate
    df = (
        df.sort_values("start_time")
          .drop_duplicates(subset="call_id", keep="last")
    )

    # Duration
    df["call_duration_seconds"] = (
        df["end_time"] - df["start_time"]
    ).dt.total_seconds()

    # Derived fields
    df["call_hour"] = df["start_time"].dt.hour

    df["call_date"] = df["start_time"].dt.date

    df["is_weekend"] = (
        df["start_time"].dt.dayofweek >= 5
    )

    # Amount imputation
    df["is_amount_imputed"] = (
        df["amount_promised"].isna()
    )

    df["amount_promised"] = (
        df["amount_promised"].fillna(0)
    )

    # Duration bucket
    df["duration_bucket"] = (
        df["call_duration_seconds"]
        .apply(duration_bucket)
    )

    # Save transformed data
    df.to_csv(
        "data/transformed_calls.csv",
        index=False
    )

    print("\nTRANSFORMATION COMPLETE")
    print("-" * 40)
    print(f"Records after transformation: {len(df)}")
    print("Output: data/transformed_calls.csv")


if __name__ == "__main__":
    main()