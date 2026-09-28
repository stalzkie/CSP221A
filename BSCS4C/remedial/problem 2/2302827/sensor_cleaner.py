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

    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")

    missing_before = df[["temperature", "humidity"]].isna().sum()

    df["station"] = df["station"].str.strip()
    df["station"] = df["station"].str.lower()

    df = df.drop_duplicates(subset=["station"], keep="first")

# temperature is the primary reading, so dropping rows that is missing
    df = df.dropna(subset=["temperature"])

# humidity is a secondary reading, so filling missing value with column's average
    humidity_avg = df["humidity"].mean()
    df["humidity"] = df["humidity"].fillna(humidity_avg)

    missing_after = df[["temperature", "humidity"]].isna().sum()

    df["status"] = df["temperature"].apply(lambda temp: "ALERT" if temp > 90 else "OK")

    df["flag"] = np.where(df["humidity"] < 40, "DRY", "NORMAL")

    df = df.reset_index(drop=True)

    return df, missing_before, missing_after


def main():
    cleaned_df, missing_before, missing_after = clean_readings(raw_rows)

    print("Missing values BEFORE cleaning:")
    print(missing_before.to_dict())
    print()

    print("Missing values AFTER cleaning:")
    print(missing_after.to_dict())
    print()

    print("Cleaned table:")
    print(cleaned_df)
    print()

    print("ALERT rows:")
    print(cleaned_df[cleaned_df["status"] == "ALERT"])
    print()

    try:
        pd.read_csv("sensor_readings.csv")
    except FileNotFoundError:
        print("Could not find sensor_readings.csv, so using the raw_rows data.")


main()