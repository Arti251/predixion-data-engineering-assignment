import sqlite3
import pandas as pd
from pathlib import Path

# Create output folder if it doesn't exist
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect("call_data.db")

# =====================================================
# Q1 - Connect Rate by Language
# =====================================================

q1 = """
SELECT
    language,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN call_outcome = 'connected' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS connect_rate
FROM calls
GROUP BY language
"""

df1 = pd.read_sql(q1, conn)

df1.to_csv(
    "output/q1_connect_rate.csv",
    index=False
)

print("\nQ1 - Connect Rate by Language")
print(df1)

# =====================================================
# Q2 - Callback Requested by Hour
# =====================================================

q2 = """
SELECT
    call_hour,
    COUNT(*) AS callback_count
FROM calls
WHERE call_outcome = 'callback_requested'
GROUP BY call_hour
ORDER BY callback_count DESC
"""

df2 = pd.read_sql(q2, conn)

df2.to_csv(
    "output/q2_callback_hour.csv",
    index=False
)

print("\nQ2 - Callback Requested by Hour")
print(df2.head())

# =====================================================
# Q3 - Long Calls Analysis
# =====================================================

q3 = """
SELECT
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM calls),
        2
    ) AS long_call_percentage,

    ROUND(
        AVG(amount_promised),
        2
    ) AS avg_amount_promised

FROM calls
WHERE duration_bucket = 'long'
"""

df3 = pd.read_sql(q3, conn)

df3.to_csv(
    "output/q3_long_calls.csv",
    index=False
)

print("\nQ3 - Long Calls Analysis")
print(df3)

# =====================================================
# Q4 - Top 3 Agents
# =====================================================

q4 = """
SELECT
    agent_id,
    COUNT(*) AS total_calls
FROM calls
GROUP BY agent_id
ORDER BY total_calls DESC
LIMIT 3
"""

df4 = pd.read_sql(q4, conn)

df4.to_csv(
    "output/q4_top_agents.csv",
    index=False
)

print("\nQ4 - Top 3 Agents")
print(df4)

# =====================================================
# Q4B - Outcome Distribution
# =====================================================

q4b = """
SELECT
    agent_id,
    call_outcome,
    COUNT(*) AS outcome_count
FROM calls
WHERE agent_id IN (
    SELECT
        agent_id
    FROM calls
    GROUP BY agent_id
    ORDER BY COUNT(*) DESC
    LIMIT 3
)
GROUP BY
    agent_id,
    call_outcome
ORDER BY
    agent_id,
    outcome_count DESC
"""

df4b = pd.read_sql(q4b, conn)

df4b.to_csv(
    "output/q4_agent_outcome_distribution.csv",
    index=False
)

print("\nQ4B - Outcome Distribution")
print(df4b)

# =====================================================
# Q5 - Call Volume Trend
# =====================================================

q5 = """
SELECT
    call_date,
    COUNT(*) AS total_calls
FROM calls
GROUP BY call_date
ORDER BY call_date
"""

df5 = pd.read_sql(q5, conn)

df5.to_csv(
    "output/q5_volume_trend.csv",
    index=False
)

print("\nQ5 - Call Volume Trend")
print(df5.head())

# =====================================================
# Close Connection
# =====================================================

conn.close()

print("\nAnalytics Complete")
print("Results saved in output/")