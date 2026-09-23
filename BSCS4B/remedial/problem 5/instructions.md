# Remedial Problem 5: Employee Training Log Auditor

## Scenario

Your HR team tracks employee training as raw log rows: an employee ID, hours completed, and a free-text list of modules taken. Some employees logged their hours twice, one entry has an unparseable value, and you need to group employees into On-Track/In-Progress/Behind buckets — then flag it if a bucket ends up too small to report on honestly.

## Data

Use this raw dataset exactly as given:

```python
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
```

- Row 3 (`e01`) is the same employee as row 1 (`E01`) once whitespace and case are normalized — a **duplicate**, kept as the first occurrence only.
- Row 4 (`E04`) has an unparseable hours value (`"N/A"`) — **dropped**, because hours completed is the core metric this audit reports on.

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | Build a `pd.DataFrame` from `raw_rows`; clean `employee_id` with `.str.strip().str.lower()`. | 1 |
| R2 | Convert `hours` with `pd.to_numeric(..., errors="coerce")`. | 1 |
| R3 | Drop duplicate employees with `drop_duplicates(subset=["employee_id"], keep="first")`. | 1 |
| R4 | Drop rows with a missing (`NaN`) hours value — documented reason: hours completed is the core metric. | 1 |
| R5 | Parse the `modules` column into a column of Python **sets** (lowercased, stripped) via `.apply()` with a `lambda`. | 1 |
| R6 | Add a `status` column via `.apply()`: `"ON_TRACK"` (hours ≥ 4), `"IN_PROGRESS"` (2 ≤ hours < 4), else `"BEHIND"`. | 1 |
| R7 | Two `assert` statements confirm the cleaning worked: no duplicate employee ids remain, and no missing hours values remain. | 2 |
| R8 | `InsufficientGroupSizeError(Exception)` is raised if any status ends up with fewer than 2 employees. | 1 |
| R9 | Using **set** operations (not string matching), find every employee whose module set contains **both** `"safety"` and `"compliance"`. | 1 |

## Suggested Build Order

Your script must stay runnable after every milestone.

- **M1 — Clean the basics.** Build the DataFrame, clean `employee_id`, convert `hours`. Print the DataFrame.
- **M2 — Duplicates and missing values.** Drop duplicates and rows with missing hours. Print the cleaned DataFrame — it should have 6 rows.
- **M3 — Sets and status.** Add the `module_set` and `status` columns. Print `status` value counts.
- **M4 — Checks and lookups.** Add both `assert` statements, the `InsufficientGroupSizeError` check, and the set-based "safety AND compliance" lookup. Print the matching employee IDs.

## Your Task

Write a Python module named **`training_log_auditor.py`** with:

- `InsufficientGroupSizeError(Exception)`
- `categorize(hours)` → `"ON_TRACK"` / `"IN_PROGRESS"` / `"BEHIND"`
- `build_training_report(rows)` → the cleaned DataFrame (raises `InsufficientGroupSizeError` if a status is too small)

## Libraries

```python
import pandas as pd
```

No NumPy or sklearn needed for this problem. You're welcome to use standard-library modules if it genuinely helps.

## What You Need to Print

Running your script should print, in order:

1. The cleaned table: `employee_id`, `hours`, `status`.
2. The status counts (`.value_counts().to_dict()`).
3. The sorted list of employee IDs whose modules include **both** `"safety"` and `"compliance"`.
4. One manual demonstration: run `build_training_report` on a 3-row dataset where one status has only 1 employee, catch `InsufficientGroupSizeError`, print it.

## Where to Review

- Building a DataFrame, `.str` methods, `pd.to_numeric`, `drop_duplicates`: Week 3 Reading Guide, Chapter 3 and Chapter 4 (§4.3–§4.5).
- `.apply()` with `lambda`: Week 3 Reading Guide, Chapter 4 (§4.7) and Chapter 1 (§1.4).
- Sets and set operations: Week 1 Reading Guide (data structures chapter).
- `assert` for sanity checks: Week 2 Reading Guide, Chapter 5 (§5.8).
- Custom exceptions: Week 2 Reading Guide, Chapter 5 (§5.5).

## Submission

Work in VS Code. 

- `training_log_auditor.py` — your complete, runnable solution.
- `writeup.md` — at least 50 words explaining how you decided a row counts as a "failure" (dropped) versus just messy-but-fixable.

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

## Before You Submit

- [ ] Runs top to bottom without errors (`python training_log_auditor.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] Both `assert` statements are present and would actually fail if the cleaning logic were broken.
- [ ] The "safety AND compliance" lookup uses a set operation (e.g. `<=` or `.issubset()`/`&`), not manual string checks.
- [ ] `writeup.md` is at least 50 words.
