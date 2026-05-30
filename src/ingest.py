import json
import pandas as pd
from datetime import datetime
from pathlib import Path

REQUIRED_FIELDS = [
    "call_id",
    "agent_id",
    "customer_phone",
    "start_time",
    "end_time",
    "call_outcome",
    "language",
    "disposition_code",
    "amount_promised",
    "retry_flag"
]


def validate_timestamp(timestamp):
    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False


def main():

    input_file = Path("data/raw_calls.json")

    with open(input_file, "r") as f:
        records = json.load(f)

    valid_records = []
    rejected_records = []

    seen_call_ids = set()

    for record in records:

        # Check missing fields
        missing_fields = [
            field
            for field in REQUIRED_FIELDS
            if field not in record
        ]

        if missing_fields:
            rejected_records.append({
                "call_id": record.get("call_id"),
                "reason": "missing_field"
            })
            continue

        # Check malformed timestamp
        if not validate_timestamp(record["start_time"]):
            rejected_records.append({
                "call_id": record.get("call_id"),
                "reason": "bad_timestamp"
            })
            continue

        # Check duplicate call_id
        if record["call_id"] in seen_call_ids:
            rejected_records.append({
                "call_id": record["call_id"],
                "reason": "duplicate"
            })
            continue

        seen_call_ids.add(record["call_id"])
        valid_records.append(record)

    # Create DataFrames
    valid_df = pd.DataFrame(valid_records)
    rejected_df = pd.DataFrame(rejected_records)

    # Save CSV outputs
    valid_df.to_csv("data/valid_records.csv", index=False)
    rejected_df.to_csv("data/rejected_log.csv", index=False)

    # Save JSON outputs
    with open("data/valid_records.json", "w") as f:
        json.dump(valid_records, f, indent=4)

    with open("data/rejected_log.json", "w") as f:
        json.dump(rejected_records, f, indent=4)

    # Summary
    print("\nINGESTION SUMMARY")
    print("-" * 40)

    print(f"Total Records: {len(records)}")
    print(f"Valid Records: {len(valid_records)}")
    print(f"Rejected Records: {len(rejected_records)}")

    breakdown = {}

    for item in rejected_records:
        reason = item["reason"]
        breakdown[reason] = breakdown.get(reason, 0) + 1

    print("\nRejection Breakdown")

    for reason, count in breakdown.items():
        print(f"{reason}: {count}")

    print("\nFiles Created:")
    print("data/valid_records.csv")
    print("data/rejected_log.csv")
    print("data/valid_records.json")
    print("data/rejected_log.json")


if __name__ == "__main__":
    main()