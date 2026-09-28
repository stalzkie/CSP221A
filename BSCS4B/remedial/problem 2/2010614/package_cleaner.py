import pandas as pd
import numpy as np

def clean_packages(rows):

    df = pd.DataFrame(rows)
    
    df["tracking_id"] = df["tracking_id"].str.strip().str.lower()
    
    df["weight_kg"] = df["weight"].str.replace("kg", "")
    df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce")
    
    missing_before = df["weight_kg"].isna().sum()

    df = df.drop_duplicates(subset=["tracking_id"], keep="first")
    
    df = df.dropna(subset=["weight_kg"])
    
    missing_after = df["weight_kg"].isna().sum()

    df["status"] = df["weight_kg"].apply(lambda w: "OVERSIZE" if w > 20 else "STANDARD")
    
    df["flag"] = np.where(df["weight_kg"] < 2, "LIGHT", "NORMAL")

    cleaned_df = df[["tracking_id", "weight_kg", "status", "flag"]]

    return cleaned_df, missing_before, missing_after

if __name__ == "__main__":
    raw_rows = [
        {"tracking_id": " PKG-001 ", "weight": "12.5kg", "destination": "Warehouse A"},
        {"tracking_id": "PKG-002", "weight": "3.2kg", "destination": "Warehouse B"},
        {"tracking_id": "pkg-001", "weight": "12.5kg", "destination": "Warehouse A"},
        {"tracking_id": "PKG-004", "weight": "heavy", "destination": "Warehouse C"},
        {"tracking_id": "PKG-005", "weight": None, "destination": "Warehouse A"},
        {"tracking_id": "PKG-006", "weight": "28.4kg", "destination": "Warehouse B"},
        {"tracking_id": "  PKG-007  ", "weight": "1.1kg", "destination": "Warehouse C"},
    ]

    cleaned_df, missing_before, missing_after = clean_packages(raw_rows)

    print(f"Missing weights before cleaning: {missing_before}")
    print(f"Missing weights after cleaning: {missing_after}")
    
    print("\nFull Cleaned Table:")
    print(cleaned_df)
    
    print("\nOVERSIZE Packages:")
    print(cleaned_df[cleaned_df["status"] == "OVERSIZE"])

    print("\nAttempting to load package_log.csv...")
    try:
        pd.read_csv("package_log.csv")
    except FileNotFoundError:
        print("Error: Couldn't find package_log.csv — check the file path.")