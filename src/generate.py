import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Reproducible output
random.seed(42)

NUM_RECORDS = 500

LANGUAGES = ["Hindi", "English", "Marathi"]

OUTCOMES = [
    "connected",
    "no_answer",
    "dropped",
    "callback_requested"
]

DISPOSITIONS = [
    "P2P",
    "FOLLOW_UP",
    "NO_RESPONSE",
    "CALL_BACK"
]


def generate_record(i):
    start = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    duration = random.randint(10, 900)
    end = start + timedelta(seconds=duration)

    return {
        "call_id": f"C{i:04d}",
        "agent_id": f"A{random.randint(1, 10):02d}",
        "customer_phone": f"9{random.randint(100000000, 999999999)}",
        "start_time": start.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end.strftime("%Y-%m-%d %H:%M:%S"),
        "call_outcome": random.choice(OUTCOMES),
        "language": random.choice(LANGUAGES),
        "disposition_code": random.choice(DISPOSITIONS),
        "amount_promised": random.choice(
            [None, 0, 500, 1000, 2000, 5000]
        ),
        "retry_flag": random.choice([True, False])
    }


def inject_missing_fields(records):
    num_missing = int(len(records) * 0.15)

    for _ in range(num_missing):
        record = random.choice(records)

        removable_fields = [
            key for key in record.keys()
            if key != "call_id"
        ]

        field = random.choice(removable_fields)

        record.pop(field, None)


def inject_bad_timestamps(records):
    num_bad = int(len(records) * 0.03)

    for _ in range(num_bad):
        record = random.choice(records)

        record["start_time"] = "INVALID_TIMESTAMP"


def inject_duplicates(records):
    num_duplicates = int(len(records) * 0.05)

    duplicates = []

    for _ in range(num_duplicates):
        duplicates.append(random.choice(records).copy())

    records.extend(duplicates)


def main():

    records = [
        generate_record(i)
        for i in range(1, NUM_RECORDS + 1)
    ]

    inject_missing_fields(records)
    inject_bad_timestamps(records)
    inject_duplicates(records)

    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "raw_calls.json"

    with open(output_file, "w") as f:
        json.dump(records, f, indent=4)

    print(f"Generated {len(records)} records")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()