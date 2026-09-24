import pandas as pd

class InsufficientGroupSizeError(Exception):
    pass

def categorize(hours):
    if hours >= 4:
        return "ON_TRACK"
    elif hours >= 2:
        return "IN_PROGRESS"
    else:
        return "BEHIND"


def build_training_report(rows):
    df = pd.DataFrame(rows)

    df['employee_id'] = df['employee_id'].str.strip().str.lower()

    df['hours'] = pd.to_numeric(df["hours"], errors="coerce")

    df = df.drop_duplicates(subset=["employee_id"], keep="first")

    # This drops the rows with missing hours since hours completed is the core metric.
    df = df.dropna(subset=["hours"])

    df["module_set"] = df["modules"].apply(
        lambda modules: set(module.strip().lower() for module in modules.split(","))
    )

    df["status"] = df["hours"].apply(categorize)

    assert df["employee_id"].is_unique
    assert df["hours"].notna().all()

    status_counts = df["status"].value_counts()

    for status, count in status_counts.items():
        if count < 2:
            raise InsufficientGroupSizeError(
                f"{status} has fewer than 2 employees"
        )
    return df

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

df = build_training_report(raw_rows)

print(df[["employee_id", "hours", "status"]])

print(df["status"].value_counts().to_dict())

required_modules = {"safety", "compliance"}

matching_employees = df[
    df["module_set"].apply(lambda modules: required_modules <= modules)
]["employee_id"].sort_values().tolist()

print(matching_employees)

test_rows = [
    {"employee_id": "E09", "hours": "5.0", "modules": "safety"},
    {"employee_id": "E10", "hours": "3.0", "modules": "ethics"},
    {"employee_id": "E11", "hours": "1.0", "modules": "compliance"}
]

try:
    build_training_report(test_rows)
except InsufficientGroupSizeError as error:
    print(error)