import pandas as pd
import numpy as np

def clean_packages(rows):
    #converting list of dicts into pandas df
    cleaned_df = pd.DataFrame(rows)
    cleaned_df.rename(columns={"weight": "weight_kg"}, inplace=True)

    #cleaning weight col
    cleaned_df["weight_kg"] = cleaned_df["weight_kg"].str.replace("kg", "")
    cleaned_df["weight_kg"] = pd.to_numeric(cleaned_df["weight_kg"], errors="coerce")

    #cleaning tracking_id col
    cleaned_df["tracking_id"] = cleaned_df["tracking_id"].str.strip()
    cleaned_df["tracking_id"] = cleaned_df["tracking_id"].str.lower()

    #checking missing weight before drop
    missing_before = cleaned_df["weight_kg"].isna().sum()
    print("\nNo. of Missing Weight Values Before:")
    print(missing_before)

    #dropping duplicates and missing
    cleaned_df = cleaned_df.drop_duplicates(subset=["tracking_id"], keep="first")
    cleaned_df = cleaned_df.dropna(subset=["weight_kg"])

    #checking missing weight after drop
    print("\nNo. of Missing Weight Values After:")
    missing_after = cleaned_df["weight_kg"].isna().sum()
    print(missing_after)

    #adding status and flag col
    cleaned_df["status"] = cleaned_df["weight_kg"].apply(lambda x: "OVERSIZE" if x > 20 else "STANDARD")
    cleaned_df["flag"] = np.where(cleaned_df["weight_kg"] < 2, "LIGHT", "NORMAL")

    #printing the cleaned and updated df
    print("\nDelivery Package Weights:")
    print(cleaned_df)

    return cleaned_df, missing_before, missing_after 


#uncleaned list of dicts
raw_rows = [
    {"tracking_id": " PKG-001 ", "weight": "12.5kg", "destination": "Warehouse A"},
    {"tracking_id": "PKG-002", "weight": "3.2kg", "destination": "Warehouse B"},
    {"tracking_id": "pkg-001", "weight": "12.5kg", "destination": "Warehouse A"},
    {"tracking_id": "PKG-004", "weight": "heavy", "destination": "Warehouse C"},
    {"tracking_id": "PKG-005", "weight": None, "destination": "Warehouse A"},
    {"tracking_id": "PKG-006", "weight": "28.4kg", "destination": "Warehouse B"},
    {"tracking_id": "  PKG-007  ", "weight": "1.1kg", "destination": "Warehouse C"},
]

#calling function
cleaned_df, missing_before, missing_after = clean_packages(raw_rows)

#error handling demo
try:
    cleaned_df = pd.read_csv("package_log.csv")
except FileNotFoundError:
    print("\nCould not find package_log.csv file. Please try again.")

#filtering only oversize
filtered_cleaned_df = cleaned_df[cleaned_df["status"] == "OVERSIZE"]
print("\nOversized Delivery Package:")
print(filtered_cleaned_df)