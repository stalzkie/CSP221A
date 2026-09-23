import pandas as pd


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

        df["respondent_id"] = (
        df["respondent_id"].str.strip().str.lower()
        )

        df["rating"] = pd.to_numeric(
                df["rating"],
                errors="coerce"
        )

        df = df.drop_duplicates(
                subset=["respondent_id"],
                keep="first"
        )

        df = df.dropna(subset=["rating"]).copy()
        df["topic_set"] = df["topics"].apply(
                lambda text: {
                        topic.strip().lower()
                        for topic in text.split(",")
                        if topic.strip()
                }
        )


        df["category"] = df["rating"].apply(categorize)

        assert not df["respondent_id"].duplicated().any()
        assert not df["rating"].isna().any()

        counts =   df["category"].value_counts()
        small_categories = counts[counts < 2]

        if not small_categories.empty:
                details = ", ".join(
                        f"{category}={count}"
                        for category, count in small_categories.items()
                )

                raise InsufficientGroupSizeError(
                        f"Category too small: {details}"
                )

        return df
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


if __name__ == "__main__":
        report = build_feedback_report(raw_rows)

        print(report[[
            "respondent_id",
            "rating",
            "category"
    ]])

        print(report["category"].value_counts().to_dict())

        required_topics = {"billing", "support"}

        matching_ids = sorted(
        report.loc[
                report["topic_set"].apply(
                        lambda topics: required_topics.issubset(topics)
                ),
                "respondent_id"
        ].tolist()
)

        print(matching_ids)

        demo_rows = [
        {"respondent_id": "D01", "rating": "5", "topics": "support"},
        {"respondent_id": "D02", "rating": "3", "topics": "ui"},
        {"respondent_id": "D03", "rating": "3", "topics": "billing"},
    ]
        try:   
         build_feedback_report(demo_rows)
        except InsufficientGroupSizeError as error:
         print(error)
