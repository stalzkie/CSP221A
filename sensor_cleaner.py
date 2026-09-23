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
    df = pd.DataFrame(rows)

    # Convert temperature and humidity to numeric values.
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")

    # Record missing values before cleaning.
    missing_before = df[["temperature", "humidity"]].isna().sum()

    # Clean station names.
    df["station"] = df["station"].str.strip().str.lower()

    # Keep the first row for duplicate stations.
    df = df.drop_duplicates(subset=["station"], keep="first")

    # Temperature is the primary reading, so remove missing temperatures.
    df = df.dropna(subset=["temperature"])

    # Humidity is secondary, so replace a missing value with the mean.
    humidity_mean = df["humidity"].mean()
    df["humidity"] = df["humidity"].fillna(humidity_mean)

    # Record missing values after cleaning.
    missing_after = df[["temperature", "humidity"]].isna().sum()

    df["status"] = df["temperature"].apply(lambda x: "ALERT" if x > 90 else "OK")
    df["flag"] = np.where(df["humidity"] < 40, "DRY", "NORMAL")
    # TODO 1:
    # Create "status" using .apply() and a lambda.
    # If temperature > 90, use "ALERT"; otherwise use "OK".

    # TODO 2:
    # Create "flag" using np.where().
    # If humidity < 40, use "DRY"; otherwise use "NORMAL".

    return df, missing_before, missing_after


cleaned_df, missing_before, missing_after = clean_readings(raw_rows)

print("Missing values before cleaning:")
print(missing_before)

print("\nMissing values after cleaning:")
print(missing_after)

print("\nCleaned sensor readings:")
print(cleaned_df)

try:
    pd.read_csv("sensor_readings.csv")
except FileNotFoundError:
    print("\nsensor_readings.csv was not found.")
