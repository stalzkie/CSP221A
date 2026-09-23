import pandas as pd


class InsufficientGroupSizeError(Exception):
    pass

def categorize(hours):
 if hours >= 4:
     return "ON TRACK"
 elif hours >= 2:
     return "IN PROGRESS"
 else:
     return "BEHIND"

def build_training_report(rows, min_group_size=2):
    df = pd.DataFrame(rows)
    df["employee_id"] = df["employee_id"].str.strip().str.lower()
    df["hours"] = pd.to_numeric(df["hours"], errors="coerce")

    df = df.drop_duplicates(
        subset=["employee_id"],
        keep="first"
    )

    df = df.dropna(subset=["hours"])

    df["module_set"] = df["modules"].apply(
        lambda m: {piece.strip().lower() for piece in m.split(",")}
    )
    df["status"] = df["hours"].apply(categorize)

    assert df["employee_id"].duplicated().sum() == 0

    assert df["hours"].isna().sum() == 0

    status_count = df["status"].value_counts().to_dict()

    small_groups = {
        status: count for status, count in status_count.items()
        if count < min_group_size
    }
    if small_groups:
        raise InsufficientGroupSizeError(
            small_groups
        )

    return df.reset_index(drop=True)

def employees_both_modules(df, module_a="safety", module_b="compliance"):
    target = {module_a, module_b}
    matches = df[df["module_set"].apply(lambda s: target <=s )]
    
    return sorted(matches["employess_id"].tolist())

if __name__ == "__main__":
 raw_rows = [
    {"employee_id": " E01 ", "hours": "4.5", "modules": "safety, compliance"},
    {"employee_id": "E02", "hours": "1.0", "modules": "safety"},
    {"employee_id": "e01", "hours": "4.5", "modules": "safety, compliance"},
    {"employee_id": "E04", "hours": "N/A", "modules": "compliance"},
    {"employee_id": "E05", "hours": "5.0", "modules": "safety, compliance, ethics"},
    {"employee_id": "E06", "hours": "2.5", "modules": "ethics"},
    {"employee_id": "E07", "hours": "0.5", "modules": "safety"},
    {"employee_id": "E08", "hours": "2.0", "modules": "ethics, safety"},
]

report = build_training_report(raw_rows)

print(report[["employee_id", "hours", "status"]])
print()

print(report["status"].value_counts().to_dict())
print()

sample_row = [
    {"employee_id": "A01", "hours": "5.0", "modules": "safety"},
    {"employee_id": "A02", "hours": "4.5", "modules": "safety"},
    {"employee_id": "A03", "hours": "1.5", "modules": "safety"},
]
try:    
    build_training_report(sample_row)
except InsufficientGroupSizeError as e:
 print("Caught expected error: {e}")