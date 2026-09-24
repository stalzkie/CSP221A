import pandas as pd

#R8
class InsufficientGroupSizeError(Exception):
    def __init__(self, category, count):
        message = f"This {category} only has {count} respodent"
        super().__init__(message)
        self.category = category
        self.count = count
#R6
def categorize(rating):
        if rating >= 4:
            return "PROMOTER"
        elif rating <= 2:
            return "DETRACTOR"
        else:
            return "PASSIVE"
        
def build_feedback_report(rows):
    #R1
    df = pd.DataFrame(rows) 
    df['respondent_id'] = df["respondent_id"].str.strip().str.lower()
    #R2
    df['rating'] = pd.to_numeric(df["rating"], errors='coerce')


    #R3&4
    clean_df = (df.drop_duplicates(subset=['respondent_id'], keep='first').dropna(subset=['rating']))

    
    #R5
    clean_df['topics'] = clean_df['topics'].apply(lambda x: {t.strip().lower() for t in x.split(",")})
    #R6
    clean_df['category'] = clean_df['rating'].apply(categorize)

    
    #R7
    assert not clean_df['respondent_id'].duplicated().any(), "There is a duplicate value"
    assert clean_df["rating"].notna().all(), "There is a missing value"
    #R8
    category_count = clean_df["category"].value_counts()
    for c, count in category_count.items():
        if count < 2:
            raise InsufficientGroupSizeError(c, count)

    
    #R9
    get_topics = {"billing", "support"}
    matched_res = clean_df[clean_df['topics'].apply(lambda x: get_topics.issubset(x))]
    sorted_res = sorted(matched_res['respondent_id'].tolist())
    
    return clean_df, sorted_res



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

three_rows = [
        {"respondent_id": " R01 ", "rating": "5", "topics": "billing, support"},
        {"respondent_id": "R02", "rating": "1", "topics": "shipping"},
        {"respondent_id": "r03", "rating": "5", "topics": "billing, support"},
]

#1.
report_df, sorted_list = build_feedback_report(raw_rows)
print(f'\nCleaned Table: \n{report_df[["respondent_id", "rating", "category"]]}\n')
#2.
print(f'Category Counts: \n{report_df["category"].value_counts().to_dict()}\n')
#3
print(f'Sorted List: \n{sorted_list}\n')
#4
try:
    small_df = build_feedback_report(three_rows)
except InsufficientGroupSizeError as e:
    print(f'{e}\n')

