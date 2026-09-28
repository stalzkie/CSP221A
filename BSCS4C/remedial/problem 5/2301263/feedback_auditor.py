import pandas as pd


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


class InsufficientGroupSizeError(Exception):
    pass


def categorize(rating):
    if rating >= 4:
        return "PROMOTER"
    elif rating <= 2:
        return "DETRACTOR"
    else:
        return "PASSIVE"


def build_feedback_report(rows):
    df = pd.DataFrame(rows)

    df["respondent_id"] = df["respondent_id"].str.strip().str.lower()

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    df = df.drop_duplicates(
        subset=["respondent_id"],
        keep="first"
    )

    df = df.dropna(
        subset=["rating"]
    )

    df["topic_set"] = df["topics"].apply(
        lambda text: {
            topic.strip().lower()
            for topic in text.split(",")
        }
    )

    df["category"] = df["rating"].apply(categorize)

    assert not df["respondent_id"].duplicated().any()
    assert df["rating"].notna().all()

    category_counts = df["category"].value_counts().to_dict()

    for category in ["PROMOTER", "DETRACTOR", "PASSIVE"]:
        count = category_counts.get(category, 0)

        if count < 2:
            raise InsufficientGroupSizeError(
                f"Category {category} has only {count} respondent(s)."
            )

    return df


cleaned_df = build_feedback_report(raw_rows)


print("CLEANED TABLE")
print(
    cleaned_df[
        ["respondent_id", "rating", "category"]
    ]
)


print("\nCATEGORY COUNTS")
print(
    cleaned_df["category"]
    .value_counts()
    .to_dict()
)


required_topics = {"billing", "support"}

matching_ids = sorted(
    cleaned_df.loc[
        cleaned_df["topic_set"].apply(
            lambda topic_set: required_topics.issubset(topic_set)
        ),
        "respondent_id"
    ].tolist()
)

print("\nBILLING AND SUPPORT RESPONDENTS")
print(matching_ids)


demo_rows = [
    {"respondent_id": "D01", "rating": "5", "topics": "billing"},
    {"respondent_id": "D02", "rating": "3", "topics": "support"},
    {"respondent_id": "D03", "rating": "3", "topics": "shipping"},
]


print("\nINSUFFICIENT GROUP SIZE DEMONSTRATION")

try:
    build_feedback_report(demo_rows)
except InsufficientGroupSizeError as error:
    print(error)