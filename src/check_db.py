import sqlite3
import pandas as pd

conn = sqlite3.connect("call_data.db")

print(pd.read_sql("SELECT COUNT(*) AS total_calls FROM calls", conn))

conn.close()