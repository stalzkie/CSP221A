import pandas as pd

class InsufficientGroupSizeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def build_training_report(rows):
    # outputs the cleaned DataFrame (raises InsufficientGroupSizeError if a status is too small)
    # R1 - build dataframe and clean
    dataset = pd.DataFrame(rows)
    dataset["employee_id"] = dataset["employee_id"].str.strip().str.lower()

    # R2 - convert hours to numeric, coerce errors to NaN
    dataset["hours"] = pd.to_numeric(dataset["hours"], errors="coerce")

    # M1 - print the dataset after initial cleaning
    # print(f"Cleaned tables:\n{dataset}\n")

    # R3 - drop duplicate employees
    dataset = dataset.drop_duplicates(subset=["employee_id"], keep="first")

    # R4 - drop rows with missing hours
    dataset = dataset.dropna(subset=["hours"])

    # R5 - parse modules column into a lowercased and stripped sets
    dataset["module_set"] = dataset["modules"].apply(lambda x: {item.strip().lower() for item in x.split(",")})

    # R6 - create status column based on hours
    dataset["status"] = dataset["hours"].apply(categorize)

    # M2 - dropped duplicates and rows with 
    # print(f":\n{dataset}\n")

    # M3 - print status value counts
    # print(f"Status counts:\n{dataset['status'].value_counts()}\n")

    # R7 - check if cleaning worked: no duplicate employee ID and no missing hour values
    assert dataset["employee_id"].is_unique, "Duplicate employee IDs found after cleaning"
    assert dataset["hours"].notna().all(), "Missing hour values found after cleaning"

    # R8 - raise InsufficientGroupSizeError if any status ends up with fewer than 2 employees
    if (dataset["status"].value_counts() < 2).any():
        raise InsufficientGroupSizeError("One or more status groups have fewer than 2 employees")

    # M4 - print matching employee IDs for set-based safety & compliance
    # print(f"Sorted list of employees with safety AND compliance modules:\n{safety_compliance_employees}\n")

    return dataset


def categorize(hours):
    if hours >= 4.0:
        return "ON_TRACK"
    elif 2.0 <= hours < 4.0:
        return "IN_PROGRESS"
    else:
        return "BEHIND"


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

    demo_rows = [
        {"employee_id": "E01", "hours": "4.5", "modules": "safety, compliance"},
        {"employee_id": "E02", "hours": "1.0", "modules": "safety"},
        {"employee_id": "E03", "hours": "4.0", "modules": "compliance"},
    ]

    cleaned_dataset = build_training_report(raw_rows)
    print(f"Cleaned table: {cleaned_dataset[['employee_id', 'hours', 'status']]}")
    print(f"Status counts: {cleaned_dataset['status'].value_counts().to_dict()}")
    
    # R9 - use set operations to find employees whose module set contains both safety and compliance
    safety_compliance_employees = cleaned_dataset[cleaned_dataset["module_set"].apply(lambda x: {"safety", "compliance"}.issubset(x))]["employee_id"].sort_values().tolist()
    print(f"Sorted list of employees with safety AND compliance modules: {safety_compliance_employees}")

    try:
        build_training_report(demo_rows)
    except InsufficientGroupSizeError as e:
        print(e)

    """
    Running your script should print, in order:

    The cleaned table: employee_id, hours, status.
    The status counts (.value_counts().to_dict()).
    The sorted list of employee IDs whose modules include both "safety" and "compliance".
    One manual demonstration: run build_training_report on a 3-row dataset where one status has only 1 employee, catch InsufficientGroupSizeError, print it.
    """