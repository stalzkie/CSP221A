#   import required libraries
import pandas as pd
import numpy as np

#   function for cleanign the package
def clean_packages(rows):
    #   M1
    #   R1 — build a dataframe from raw_rows 
    df = pd.DataFrame(rows)

    #   R3 - strip the kg using replace() then convert it using to_numeric with coerce
    df["weight_kg"] = df["weight"].str.replace("kg", "", regex=False)
    df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce")

    #   R9 - count missing_before weights
    missing_before = df["weight_kg"].isna().sum()  

    #   M2
    #   R2 - clean th e tracking_id with str.strip() and str.lower()
    df["tracking_id"] = df["tracking_id"].str.strip().str.lower()
    #print the dataframe
    #print(df)

    #   M3
    #   R4 - drop the duplicated packages
    df = df.drop_duplicates(subset=["tracking_id"], keep="first")

    #   R5 - drop missing weights because weight is the field this pipeline exists to validates
    df = df.dropna(subset=["weight_kg"])
    
    #   R9 - count missing_after weights
    missing_after = df["weight_kg"].isna().sum()     

    #   M4
    #   R6 - classify the packages in their weights
    df["status"] = df["weight_kg"].apply(
        lambda weight: "OVERSIZE" if weight > 20 else "STANDARD"
    )

    #   R7 - flag the packages based in their weights
    df["flag"] = np.where(
        df["weight_kg"] < 2,
        "LIGHT",
        "NORMAL"
    )

    cleaned_df = df[["tracking_id", "weight_kg", "status", "flag"]]

    # M5 check - print only OVERSIZE rows using boolean filtering
    # oversize_rows = cleaned_df[cleaned_df["status"] == "OVERSIZE"]
    # print(oversize_rows)

    return cleaned_df, missing_before, missing_after

if __name__ == "__main__":

    #   given data
    raw_rows = [
        {"tracking_id": " PKG-001 ", "weight": "12.5kg", "destination": "Warehouse A"},
        {"tracking_id": "PKG-002", "weight": "3.2kg", "destination": "Warehouse B"},
        {"tracking_id": "pkg-001", "weight": "12.5kg", "destination": "Warehouse A"},
        {"tracking_id": "PKG-004", "weight": "heavy", "destination": "Warehouse C"},
        {"tracking_id": "PKG-005", "weight": None, "destination": "Warehouse A"},
        {"tracking_id": "PKG-006", "weight": "28.4kg", "destination": "Warehouse B"},
        {"tracking_id": "  PKG-007  ", "weight": "1.1kg", "destination": "Warehouse C"},
    ]

    #   run the cleaning function 
    cleaned_df, missing_before, missing_after = clean_packages(raw_rows)

    # print in order
    print(f"Missing weight before cleaning: {missing_before}")
    print(f"Missing weight after cleaning: {missing_after}")
    print(cleaned_df)

    #   R8 - load a missing file but handle it without crashing then print
    try:
        pd.read_csv("package_log.csv")
    except FileNotFoundError:
        print("package_log.csv was not found")