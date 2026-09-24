import pandas as pd
import numpy as np

raw_rows = [
    {"tracking_id": " PKG-001 ", "weight": "12.5kg", "destination": "Warehouse A"},
    {"tracking_id": "PKG-002", "weight": "3.2kg", "destination": "Warehouse B"},
    {"tracking_id": "pkg-001", "weight": "12.5kg", "destination": "Warehouse A"},
    {"tracking_id": "PKG-004", "weight": "heavy", "destination": "Warehouse C"},
    {"tracking_id": "PKG-005", "weight": None, "destination": "Warehouse A"},
    {"tracking_id": "PKG-006", "weight": "28.4kg", "destination": "Warehouse B"},
    {"tracking_id": "  PKG-007  ", "weight": "1.1kg", "destination": "Warehouse C"},
]


def clean_packages(rows):
    #load the rows into a dataframe
    df = pd.DataFrame(rows)

    #remove the "kg" then convert to numbers
    #errors="coerce" turns "heavy" and None into NaN so it wont crash
    df["weight_kg"] = df["weight"].str.replace("kg", "")
    df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce")

    missing_before = df["weight_kg"].isna().sum()

    #fix the tracking ids 
    df["tracking_id"] = df["tracking_id"].str.strip().str.lower()

    #pkg-001 was scanned twice, keep only the first one
    df = df.drop_duplicates(subset=["tracking_id"], keep="first")

    #drop rows with no weight 
    df = df.dropna(subset=["weight_kg"])

    missing_after = df["weight_kg"].isna().sum()

    #derived columns
    df["status"] = df["weight_kg"].apply(lambda w: "OVERSIZE" if w > 20 else "STANDARD")
    df["flag"] = np.where(df["weight_kg"] < 2, "LIGHT", "NORMAL")

    #only keep the columns we need
    cleaned_df = df[["tracking_id", "weight_kg", "status", "flag"]]

    return cleaned_df, missing_before, missing_after


# run cleaner, print results
cleaned, before, after = clean_packages(raw_rows)

print("Missing weight count before cleaning:", before)
print("Missing weight count after cleaning:", after)

print("\nCleaned table:")
print(cleaned)

# boolean filter for oversize packages
print("\nOVERSIZE packages only:")
print(cleaned[cleaned["status"] == "OVERSIZE"])

# try loading a csv that doesnt exist
print()
try:
    log = pd.read_csv("package_log.csv")
    print(log)
except FileNotFoundError:
    print("Error: package_log.csv was not found. Skipping the CSV load.")