# Remedial Problem 2: Delivery Package Weight Cleaner

## Scenario

A regional delivery hub logs package weights as they're scanned. The raw export is a list of dicts pulled from handheld scanners — tracking IDs have inconsistent capitalization and stray whitespace, weights are recorded as text with a `"kg"` suffix, some are unreadable, and one package was scanned twice. You need to clean it into a usable table with Pandas before routing decisions can be made.

## Data

Use this raw dataset exactly as given:

```python
raw_rows = [
    {"tracking_id": " PKG-001 ", "weight": "12.5kg", "destination": "Warehouse A"},
    {"tracking_id": "PKG-002", "weight": "3.2kg", "destination": "Warehouse B"},
    {"tracking_id": "pkg-001", "weight": "12.5kg", "destination": "Warehouse A"},
    {"tracking_id": "PKG-004", "weight": "heavy", "destination": "Warehouse C"},
    {"tracking_id": "PKG-005", "weight": None, "destination": "Warehouse A"},
    {"tracking_id": "PKG-006", "weight": "28.4kg", "destination": "Warehouse B"},
    {"tracking_id": "  PKG-007  ", "weight": "1.1kg", "destination": "Warehouse C"},
]
```

- Row 3 (`pkg-001`) is the same package as row 1 (`PKG-001`) once whitespace and case are normalized — a **duplicate**, kept as the *first* occurrence, dropped otherwise.
- Row 4 (`PKG-004`) has an unparseable weight (`"heavy"`) — **dropped**, because weight is the field this pipeline exists to validate.
- Row 5 (`PKG-005`) has a missing weight (`None`) — also **dropped**, for the same reason.

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | Build a `pd.DataFrame` from `raw_rows`. | 1 |
| R2 | The `tracking_id` column is cleaned with `.str.strip()` and `.str.lower()`. | 1 |
| R3 | The `"kg"` suffix is stripped from `weight` with `.str.replace()`, then converted with `pd.to_numeric(..., errors="coerce")` so unparseable/missing values become `NaN` instead of crashing. | 2 |
| R4 | Duplicate packages (same cleaned tracking ID) are removed with `drop_duplicates(subset=["tracking_id"], keep="first")`. | 1 |
| R5 | Rows with a missing (`NaN`) `weight_kg` are dropped — documented reason: weight is the field this pipeline exists to validate. | 1 |
| R6 | A `status` column is added via `.apply()` with a `lambda`: `"OVERSIZE"` if `weight_kg > 20`, else `"STANDARD"`. | 1 |
| R7 | A `flag` column is added via `np.where()`: `"LIGHT"` if `weight_kg < 2`, else `"NORMAL"`. | 1 |
| R8 | Loading a CSV (`package_log.csv`, which does not exist) is attempted inside a `try/except FileNotFoundError`, printing a clear message instead of crashing. | 1 |
| R9 | The count of missing `weight_kg` values is printed **before** and **after** the cleaning steps (duplicates, drop). | 1 |

## Suggested Build Order

Your script must stay runnable after every milestone.

- **M1 — Load and parse weight.** Build the DataFrame. Strip `"kg"` and convert to numeric. Print the missing-value count *before* any cleaning.
- **M2 — Strings.** Clean the `tracking_id` column with `.str.strip().str.lower()`. Print the DataFrame.
- **M3 — Duplicates and missing values.** Drop duplicate tracking IDs, then drop rows with missing weight. Print the missing-value count again — it should now be zero.
- **M4 — Derived columns.** Add `status` and `flag`. Print the full cleaned table.
- **M5 — Filtering and error handling.** Print only the `OVERSIZE` rows using boolean filtering. Add the `try/except FileNotFoundError` demo.

## Your Task

Write a Python module named **`package_cleaner.py`** with:

- `clean_packages(rows)` → returns `(cleaned_df, missing_before, missing_after)`

## Libraries

```python
import pandas as pd
import numpy as np
```

You're welcome to use any other standard-library module if it genuinely helps. No sklearn for this remedial set.

## What You Need to Print

Running your script should print, in order:

1. Missing-weight count **before** cleaning.
2. Missing-weight count **after** cleaning (should be 0).
3. The full cleaned table (tracking_id, weight_kg, status, flag).
4. The `FileNotFoundError` demo message from attempting to load `package_log.csv`.

## Where to Review

- Building a DataFrame, `.str` methods (including `.str.replace()`): Week 3 Reading Guide, Chapter 3 (§3.1) and Chapter 4 (§4.5).
- `pd.to_numeric(errors="coerce")`: Week 3 Reading Guide, Chapter 4 (§4.4).
- `isna()`, `dropna()`, `drop_duplicates()`: Week 3 Reading Guide, Chapter 4 (§4.1–§4.3).
- `.apply()` with `lambda`, `np.where()`: Week 3 Reading Guide, Chapter 4 (§4.7) and Chapter 2 (§2.7).
- Catching `FileNotFoundError` specifically: Week 3 Reading Guide, §3.2; Week 2 Reading Guide, Chapter 5 (§5.3).

## Submission

Work in VS Code.

- `package_cleaner.py` — your complete, runnable solution.
- `writeup.md` — at least 50 words explaining why both the unparseable row and the missing-weight row were dropped rather than filled in.

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

## Before You Submit

- [ ] Runs top to bottom without errors (`python package_cleaner.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] The "after" missing-weight count is actually 0.
- [ ] The duplicate `pkg-001` row does not appear twice in your final output.
- [ ] `writeup.md` is at least 50 words.
