import pandas as pd
import numpy as np

def clean_readings(rows):
    df = pd.DataFrame(rows)

    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")

    missing_before = df[["temperature", "humidity"]].isna().sum()

    df["station"] = df["station"].str.strip().str.lower()

    df = df.drop_duplicates(subset=["station"], keep="first")

    df = df.dropna(subset=["temperature"])

    df["humidity"] = df["humidity"].fillna(df["humidity"].mean())

    missing_after = df[["temperature", "humidity"]].isna().sum()

    df["status"] = df["temperature"].apply(lambda x: "ALERT" if x > 90 else "OK")

    df["flag"] = np.where(df["humidity"] < 40, "DRY", "NORMAL")

    return df, missing_before, missing_after

if __name__ == "__main__":
    raw_rows = [
        {"station": " North Hill ", "temperature": "72", "humidity": "45"},
        {"station": "South Bay", "temperature": "101", "humidity": "38"},
        {"station": "north hill", "temperature": "75", "humidity": "50"},
        {"station": "East Ridge", "temperature": "not_a_number", "humidity": "60"},
        {"station": "West Point", "temperature": "68", "humidity": "N/A"},
        {"station": "Lake View", "temperature": "95", "humidity": "42"},
        {"station": "  Hilltop  ", "temperature": "59", "humidity": "70"},
    ]

    cleaned_df, missing_before, missing_after = clean_readings(raw_rows)

    print(missing_before)
    print(missing_after)
    print(cleaned_df)

    try:
        pd.read_csv("sensor_readings.csv")
    except FileNotFoundError:
        print("Error: 'sensor_readings.csv' could not be found.")