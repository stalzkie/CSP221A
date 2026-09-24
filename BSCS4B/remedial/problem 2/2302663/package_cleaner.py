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
    df = pd.DataFrame(rows)

    df["weight_kg"] = df["weight"].str.replace("kg", "", regex=False)
    df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce")

    missing_before = df["weight_kg"].isnull().sum()
    print(f"Missing-weight count before cleaning: {missing_before}")

    df["tracking_id"] = df["tracking_id"].str.strip().str.lower()

    df = df.drop_duplicates(subset=["tracking_id"], keep="first")
    df = df.dropna(subset=["weight_kg"])

    missing_after = df["weight_kg"].isnull().sum()
    print(f"Missing-weight count after cleaning: {missing_after}")

    df["status"] = df["weight_kg"].apply(lambda weight: "OVERSIZE" if weight > 20 else "STANDARD" )

    df["flag"] = np.where(df["weight_kg"] < 2, "LIGHT", "NORMAL")

    print(df[["tracking_id", "weight_kg", "status", "flag"]])
    print("OVERSIZE packages:")
    print(df[df["status"] == "OVERSIZE"]) 

    try: csv_df = pd.read_csv("package_log.csv")
    except FileNotFoundError:
        print("package_log.csv was not found")

    return df, missing_before, missing_after

if __name__ == "__main__":
    clean_packages(raw_rows)

