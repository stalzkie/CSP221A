import pandas as pd #Library for DataFrame

class InsufficientGroupSizeError(Exception):
    pass

def categorize(hours): #Sets and status
    if hours >=4.0:
        return "ON_TRACK"
    elif hours >=2.0:
        return "IN_PROGRESS"
    else:
        return "BEHIND"

#M1 Clean the basics
def build_training_report(rows):
    df = pd.DataFrame(rows) # Dataframe from raw_rows

    df['employee_id'] = df['employee_id'].str.strip().str.lower() # ID cleaned

    df['hours'] = pd.to_numeric(df['hours'], errors='coerce') #hours converted to numeric
#M2 Drop and clean duplicates and missing value
    df = df.drop_duplicates(subset=['employee_id'], keep = 'first') # drop duplicated employee id

    df = df.dropna(subset=['hours']) #drop rows with missing hours value
#M3 Sets and status 
    df['module_set'] = df['modules'].apply(lambda module_string: set(topic.strip().lower() for topic in module_string.split(',')))

    df['status'] = df['hours'].apply(categorize)
#M4 Check for errors
    assert df['employee_id'].duplicated().sum() == 0
    assert df['hours'].isna().sum() == 0


    status_counts = df['status'].value_counts()
    for status_name, count in status_counts.items():
        if count < 2:
            raise InsufficientGroupSizeError(f"Bucket '{status_name}' is too small: only {count} employee(s).")
    return df
 
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
    
final_df = build_training_report(raw_rows)

print(final_df[['employee_id', 'hours', 'status']].to_string(index=False)) #Cleaned Table
print(final_df['status'].value_counts().to_dict()) #Status Counts

required_topics = {"safety", "compliance"}

matching_staff = final_df[final_df['module_set'].apply(lambda module_set: required_topics.issubset(module_set))]
fully_trained_ids = sorted(matching_staff['employee_id'].tolist())
print(fully_trained_ids)

bad_datasets = [
    {"employee_id": "T01", "hours": "4.5", "modules": "safety"},
    {"employee_id": "T02", "hours": "5.0", "modules": "compliance"},
    {"employee_id": "T03", "hours": "1.0", "modules": "ethics"}
]

try:
    build_training_report(bad_datasets)
except InsufficientGroupSizeError as custom_err:
    print(f"Succesfully caught error: {custom_err}")
