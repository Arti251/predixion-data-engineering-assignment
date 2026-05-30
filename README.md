# Predixion AI Data Engineering Assignment

## Overview

This project simulates an end-to-end ETL pipeline for voice agent call logs.

The pipeline:

1. Generates synthetic call records
2. Validates and ingests raw JSON data
3. Cleans and transforms records
4. Loads processed data into SQLite
5. Performs analytical reporting

## Project Structure

```text
data/
output/
src/
call_data.db
README.md
requirements.txt
```

## Tech Stack

- Python
- Pandas
- SQLite

## How to Run

### Generate Data

python3 src/generate.py

### Ingest and Validate

python3 src/ingest.py

### Transform

python3 src/transform.py

### Load to SQLite

python3 src/load.py

### Run Analytics

python3 src/queries.py

## Outputs

Analytics CSVs are generated in:

output/

## Design Decisions

- Pandas used for transformations.
- SQLite used for lightweight local storage.
- Idempotent loading achieved using table replacement.
- Rejected records stored separately for data quality monitoring.