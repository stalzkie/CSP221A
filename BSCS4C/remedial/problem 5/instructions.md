# Remedial Problem 5: Customer Feedback Response Auditor

## Scenario

Your team collects customer feedback as raw survey rows: a respondent ID, a 1–5 rating, and a free-text list of topics the customer mentioned. Some respondents submitted twice, one rating is unparseable, and you need to group respondents into Promoter/Passive/Detractor buckets — then flag it if a bucket ends up too small to report on honestly.

## Data

Use this raw dataset exactly as given:

```python
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
```

- Row 3 (`r01`) is the same respondent as row 1 (`R01`) once whitespace and case are normalized — a **duplicate**, kept as the first occurrence only.
- Row 4 (`R04`) has an unparseable rating (`"not_rated"`) — **dropped**, because rating is the core metric this audit reports on.

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | Build a `pd.DataFrame` from `raw_rows`; clean `respondent_id` with `.str.strip().str.lower()`. | 1 |
| R2 | Convert `rating` with `pd.to_numeric(..., errors="coerce")`. | 1 |
| R3 | Drop duplicate respondents with `drop_duplicates(subset=["respondent_id"], keep="first")`. | 1 |
| R4 | Drop rows with a missing (`NaN`) rating — documented reason: rating is the core metric. | 1 |
| R5 | Parse the `topics` column into a column of Python **sets** (lowercased, stripped) via `.apply()` with a `lambda`. | 1 |
| R6 | Add a `category` column via `.apply()`: `"PROMOTER"` (rating ≥ 4), `"DETRACTOR"` (rating ≤ 2), else `"PASSIVE"`. | 1 |
| R7 | Two `assert` statements confirm the cleaning worked: no duplicate respondent ids remain, and no missing ratings remain. | 2 |
| R8 | `InsufficientGroupSizeError(Exception)` is raised if any category ends up with fewer than 2 respondents. | 1 |
| R9 | Using **set** operations (not string matching), find every respondent whose topic set contains **both** `"billing"` and `"support"`. | 1 |

## Suggested Build Order

Your script must stay runnable after every milestone.

- **M1 — Clean the basics.** Build the DataFrame, clean `respondent_id`, convert `rating`. Print the DataFrame.
- **M2 — Duplicates and missing values.** Drop duplicates and rows with missing rating. Print the cleaned DataFrame — it should have 6 rows.
- **M3 — Sets and categories.** Add the `topic_set` and `category` columns. Print `category` value counts.
- **M4 — Checks and lookups.** Add both `assert` statements, the `InsufficientGroupSizeError` check, and the set-based "billing AND support" lookup. Print the matching respondent IDs.

## Your Task

Write a Python module named **`feedback_auditor.py`** with:

- `InsufficientGroupSizeError(Exception)`
- `categorize(rating)` → `"PROMOTER"` / `"DETRACTOR"` / `"PASSIVE"`
- `build_feedback_report(rows)` → the cleaned DataFrame (raises `InsufficientGroupSizeError` if a category is too small)

## Libraries

```python
import pandas as pd
```

No NumPy or sklearn needed for this problem. You're welcome to use standard-library modules if it genuinely helps.

## What You Need to Print

Running your script should print, in order:

1. The cleaned table: `respondent_id`, `rating`, `category`.
2. The category counts (`.value_counts().to_dict()`).
3. The sorted list of respondent IDs whose topics include **both** `"billing"` and `"support"`.
4. One manual demonstration: run `build_feedback_report` on a 3-row dataset where one category has only 1 respondent, catch `InsufficientGroupSizeError`, print it.

## Where to Review

- Building a DataFrame, `.str` methods, `pd.to_numeric`, `drop_duplicates`: Week 3 Reading Guide, Chapter 3 and Chapter 4 (§4.3–§4.5).
- `.apply()` with `lambda`: Week 3 Reading Guide, Chapter 4 (§4.7) and Chapter 1 (§1.4).
- Sets and set operations: Week 1 Reading Guide (data structures chapter).
- `assert` for sanity checks: Week 2 Reading Guide, Chapter 5 (§5.8).
- Custom exceptions: Week 2 Reading Guide, Chapter 5 (§5.5).

## Submission

Work in VS Code

- `feedback_auditor.py` — your complete, runnable solution.
- `writeup.md` — at least 50 words explaining how you decided a row counts as a "failure" (dropped) versus just messy-but-fixable.

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

## Before You Submit

- [ ] Runs top to bottom without errors (`python feedback_auditor.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] Both `assert` statements are present and would actually fail if the cleaning logic were broken.
- [ ] The "billing AND support" lookup uses a set operation (e.g. `<=` or `.issubset()`/`&`), not manual string checks.
- [ ] `writeup.md` is at least 50 words.
