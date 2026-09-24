import pandas as pd 
import numpy as np 

# Write-up:
# I dropped rows where the weight was missing or could not be parsed
# because the weight is needed to determine the package status and the flag,
# and "heavy" could not be converted into a number, and the missing weight
# does not provide enough information to calculate those fields safely. It
# would be wrong to fill in a weight because it would be inventing a value
# that was not present in the data. Dropping the rows with missing weight
# maintains the integrity of the data.

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
    df = pd.DataFrame(rows)
    df["weight_kg"] = df["weight"].str.replace("kg","", regex=False)
    df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce")
    missing_before = df["weight_kg"].isna().sum()

    df["tracking_id"] = df["tracking_id"].str.strip().str.lower()

    df = df.drop_duplicates(subset=["tracking_id"], keep="first")
    df = df.dropna(subset=["weight_kg"])
    missing_after = df["weight_kg"].isna().sum()

    df["status"] = df["weight_kg"].apply(lambda weight: "OVERSIZE" if weight > 20 else "STANDARD")
    df["flag"] = np.where(df["weight_kg"] < 2, "LIGHT", "NORMAL")
    return df, missing_before, missing_after
    
cleaned_df, missing_before, missing_after = clean_packages(raw_rows)
print("Missing-weight count before cleaning:", missing_before)
print("Missing-weight count after cleaning:", missing_after)
print(cleaned_df[["tracking_id", "weight_kg", "status", "flag"]])
print(cleaned_df[cleaned_df["status"] == "OVERSIZE"])
try:
    package_log = pd.read_csv("package_log.csv")
except FileNotFoundError:
    print("package_log.csv was not found; continuing without it.")