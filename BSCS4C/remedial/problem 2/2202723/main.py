import pandas as pd
import numpy as np

raw_rows = [
    {"station": " North Hill ", "temperature": "72", "humidity": "45"},
    {"station": "South Bay", "temperature": "101", "humidity": "38"},
    {"station": "north hill", "temperature": "75", "humidity": "50"},
    {"station": "East Ridge", "temperature": "not_a_number", "humidity": "60"},
    {"station": "West Point", "temperature": "68", "humidity": "N/A"},
    {"station": "Lake View", "temperature": "95", "humidity": "42"},
    {"station": "  Hilltop  ", "temperature": "59", "humidity": "70"},
]

def clean_readings(rows):
    # Build a `pd.DataFrame` from `raw_rows`. 
    df = pd.DataFrame(rows)

    # The `station` column is cleaned with `.str.strip()` and `.str.lower()`. | 1 |
    df['station'] = df['station'].str.strip().str.lower()

    # `temperature` and `humidity` are converted with `pd.to_numeric(..., errors="coerce")` so unparseable values become `NaN` instead of crashing the script. | 1 |
    df['temperature'] = pd.to_numeric(df['temperature'], errors="coerce")
    df['humidity'] = pd.to_numeric(df['humidity'], errors="coerce")

    # `isna().sum()` for `temperature` and `humidity` is printed **before** and **after** the cleaning steps (duplicates, drop, fill). | 1 |
    missing_before = df[['temperature', 'humidity']].isna().sum()

    # Duplicate stations (same cleaned name) are removed with `drop_duplicates(subset=["station"], keep="first")`
    df = df.drop_duplicates(subset=['station'], keep='first')

    # Rows with a missing (`NaN`) `temperature` are dropped — documented reason: temperature is the primary reading.
    df = df.dropna(subset=['temperature'])

    # Rows with a missing `humidity` are **not** dropped — instead, `humidity` is filled with `df["humidity"].mean()` — documented reason: humidity is a secondary reading.
    df['humidity'] = df['humidity'].fillna(df['humidity'].mean())

    # `isna().sum()` for `temperature` and `humidity` is printed **before** and **after** the cleaning steps (duplicates, drop, fill). | 1 |
    missing_after = df[['temperature', 'humidity']].isna().sum()

    # A `status` column is added via `.apply()` with a `lambda`: `"ALERT"` if `temperature > 90`, else `"OK"`. | 1 |
    df['status'] = df.apply(lambda x: 'ALERT' if x['temperature'] > 90 else 'OK', axis=1)

    #A `flag` column is added via `np.where()`: `"DRY"` if `humidity < 40`, else `"NORMAL"`.
    df['flag'] = np.where(df['humidity'] < 40, "DRY", "NORMAL")

    return df, missing_before, missing_after

cleaned_df, missing_before, missing_after = clean_readings(raw_rows)

print("Before Cleaning:")
print(missing_before)

print("After Cleaning:")
print(missing_after)

print(cleaned_df)

print("ALERT rows:")
print(cleaned_df[cleaned_df['status'] == 'ALERT'])

# Loading a CSV (`sensor_readings.csv`, which does not exist) is attempted inside a `try/except FileNotFoundError`, printing a clear message instead of crashing. | 1 |
try:
    pd.read_csv('sensor_readings.csv')
except FileNotFoundError:
    print("Oops! The file does not exist in this directory.\n")