import pandas as pd

MIN_GROUP_SIZE = 2
CATEGORIES = ["PROMOTER", "PASSIVE", "DETRACTOR"]

class InsufficientGroupSizeError(Exception):
    pass

raw_rows = [
    {"respondent_id": " R01 ", "rating": "5", "topics": "billing, support"},
    {"respondent_id": "R02", "rating": "2", "topics": "shipping"},
    {"respondent_id": "r01", "rating": "5", "topics": "billing, support"},
    {"respondent_id": "R04", "rating": "not_rated", "topics": "support"},
    {"respondent_id": "R05", "rating": "4", "topics": "billing, support, ui"},
    {"respondent_id": "R06", "rating": "3", "topics": "ui"},
    {"respondent_id": "R07", "rating": "1", "topics": "shipping, billing"},
    {"respondent_id": "R08", "rating": "3", "topics": "ui, billing"},
]

def categorize(rating):
    if rating >= 4:
        return "PROMOTER"
    if rating <= 2:
        return "DETRACTOR"
    return "PASSIVE"

def build_feedback_report(raw_rows):
    df = pd.DataFrame(raw_rows)
    df['respondent_id'] = df['respondent_id'].str.strip().str.lower()
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.drop_duplicates(subset='respondent_id', keep='first')
    df = df.dropna(subset=['rating'])
    df['category'] = df['rating'].apply(categorize)
    df["topic_set"] = df["topics"].apply(lambda t: {t.lower().strip() for t in t.split(',')})

    assert not df["respondent_id"].duplicated().any(), "There are still duplicate respondent ids."
    assert not df["rating"].isna().any(), "There are still missing ratings."

    counts = df["category"].value_counts()
    for category in CATEGORIES:
        count = counts.get(category, 0)
        if count < MIN_GROUP_SIZE:
            raise InsufficientGroupSizeError(f"Insufficient group size for category: {category} ({count})")

    return df

df = build_feedback_report(raw_rows)

required = {"billing", "support"}
mask = df["topic_set"].apply(lambda s: required <= s)
billing_and_support = sorted(df.loc[mask, "respondent_id"])

print(df[["respondent_id", "rating", "category"]])
print(df["category"].value_counts().to_dict())
print(billing_and_support)

small_rows = [
    {"respondent_id": "A1", "rating": "5", "topics": "ui"},
    {"respondent_id": "A2", "rating": "5", "topics": "billing"},
    {"respondent_id": "A3", "rating": "1", "topics": "shipping"},
]

try:
    build_feedback_report(small_rows)
except InsufficientGroupSizeError as e:
    print(e)

# print(df)