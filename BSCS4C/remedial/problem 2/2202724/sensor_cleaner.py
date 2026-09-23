import pandas as pd
import numpy as np

# Raw Data

raw_rows = [
    {"station": " North Hill ", "temperature": "72", "humidity": "45"},
    {"station": "South Bay", "temperature": "101", "humidity": "38"},
    {"station": "north hill", "temperature": "75", "humidity": "50"},
    {"station": "East Ridge", "temperature": "not_a_number", "humidity": "60"},
    {"station": "West Point", "temperature": "68", "humidity": "N/A"},
    {"station": "Lake View", "temperature": "95", "humidity": "42"},
    {"station": "  Hilltop  ", "temperature": "59", "humidity": "70"},
]

# The clean reading function
def clean_reading(rows):
    # Build a DataFrame from the rows
    df = pd.DataFrame(rows)

    # Cleaning the station strings
    df['station'] = df['station'].str.strip().str.lower()

    # Converting temperature and humidity to numeric, coercing errors to NaN
    df['temperature'] = pd.to_numeric(df["temperature"], errors='coerce')
    df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')

    # Missing value before cleaning
    missing_before = df[["temperature", "humidity"]].isnull().sum().copy()

    # Dropping the duplicate stations
    df = df.drop_duplicates(subset='station', keep='first')

    # Drop rows with a missing temperature
    df = df.dropna(subset=['temperature'])

    # Fill missing humidity with the column mean
    humidity_mean = df['humidity'].mean()
    df['humidity'] = df['humidity'].fillna(humidity_mean)

    # Count the missing values after cleaning
    missing_after = df[["temperature", "humidity"]].isnull().sum().copy()

    # Return alert with via .apply() with a lambda
    df['status'] = df ['temperature'].apply(lambda x: 'alert' if x > 90 else 'ok')

    # Flag column using np.where() to flag high humidity
    df['flag'] = np.where(df['humidity'] < 40, 'dry', 'normal')

    df = df.reset_index(drop=True)
    return df, missing_before, missing_after

# Exception Handling for unexistent csv file

def load_csv_demo(path="sensor_readings.csv"):
    try:
        df = pd.read_csv(path)
        print(f"Loaded {len(df)} rows from {path}")
        return df
    except FileNotFoundError:
        print(f"Attention: Could not find '{path}' -- skiiping CSV load and using the " f"built-in raw data instead.")
        return None

if __name__ == "__main__":

    cleaned_df, missing_before, missing_after = clean_reading(raw_rows)

    print("Missing values before cleaning:")
    print(missing_before)
    print()

    print("Missing values after cleaning:")
    print(missing_after)
    print()

    print("Cleaned sensor readings:")
    print(cleaned_df)
    print()


    print("Alert rows only (temperature > 90):")
    alert_rows = cleaned_df[cleaned_df['status'] == 'alert']
    print(alert_rows)
    print()

    print("CSV load demo:")
    load_csv_demo("sensor_readings.csv")