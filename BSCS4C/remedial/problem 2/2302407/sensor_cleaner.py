import numpy as np
import pandas as pd

raw_rows = [
    {"station": " North Hill ", "temperature": "72", "humidity": "45"},
    {"station": "South Bay", "temperature": "101", "humidity": "38"},
    {"station": "north hill", "temperature": "75", "humidity": "50"},
    {"station": "East Ridge", "temperature": "not_a_number", "humidity": "60"},
    {"station": "West Point", "temperature": "68", "humidity": "N/A"},
    {"station": "Lake View", "temperature": "95", "humidity": "42"},
    {"station": "  Hilltop  ", "temperature": "59", "humidity": "70"},
]


def clean_data(raw_rows):
    # R1
    df = pd.DataFrame(raw_rows)
    print("=======================")
    print("BEFORE CLEANING")
    print(df["temperature"])
    print(df["humidity"])
    print("=======================")

    # R2
    df["station"] = df["station"].str.strip().str.lower()

    # R3 temperature and humidity are converted with pd.to_numeric(..., errors="coerce") so unparseable values become NaN instead of crashing the script.
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
    temp_missing_count = df["temperature"].isna().sum()
    humid_missing_count = df["humidity"].isna().sum()
    print("temperature missing count: ", temp_missing_count)
    print("humidity missing count: ", humid_missing_count)
    print("")
    print("")

    # R4 - 	Duplicate stations (same cleaned name) are removed with drop_duplicates(subset=["station"], keep="first").
    df = df.drop_duplicates(subset=["station"], keep="first")

    # R5 - Rows with a missing (NaN) temperature are dropped — documented reason: temperature is the primary reading.
    df = df.dropna(subset=["temperature"])

    # R6	Rows with a missing humidity are not dropped — instead, humidity is filled with df["humidity"].mean() — documented reason: humidity is a secondary reading.
    humidity_mean = df["humidity"].mean()
    df["humidity"] = df["humidity"].fillna(humidity_mean)

    # R7 -  A status column is added via .apply() with a lambda: "ALERT" if temperature > 90, else "OK".
    df["status"] = df["temperature"].apply(lambda t: "OK" if t > 90 else "ALERT")

    # R8 A flag column is added via np.where(): "DRY" if humidity < 40, else "NORMAL".

    df["flag"] = df["humidity"].apply(lambda h: np.where(h < 40, "DRY", "NORMAL"))
    print("=======================")
    print("AFTER CLEANING")
    print(df["temperature"])
    print(df["humidity"])
    print("=======================")
    temp_missing_count = df["temperature"].isna().sum()
    humid_missing_count = df["humidity"].isna().sum()
    print("temperature missing count: ", temp_missing_count)
    print("humidity missing count: ", humid_missing_count)
    print("")
    print("")
    print(df)


if __name__ == "__main__":
    clean_data(raw_rows)
    try:
        with open("sensor_readings.csv") as f:
            f = f.read()

    except FileNotFoundError as e:
        print("File is not found: ", e)


# Running your script should print, in order:
#
# Missing-value counts for temperature and humidity before cleaning.
# Missing-value counts for temperature and humidity after cleaning (should be 0 for both).
# The full cleaned table (station, temperature, humidity, status, flag).
# The FileNotFoundError demo message from attempting to load sensor_readings.csv.
