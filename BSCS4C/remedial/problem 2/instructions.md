# Remedial Problem 2: Sensor Reading Cleaner

## Scenario

A small weather-monitoring network reports temperature and humidity readings from field stations once a day. The raw export is a list of dicts pulled straight from the devices — station names have inconsistent capitalization and stray whitespace, some readings are unparseable text, and one station reported twice. You need to clean it into a usable table with Pandas before anyone can look at it.

## Data

Use this raw dataset exactly as given:

```python
raw_rows = [
    {"station": " North Hill ", "temperature": "72", "humidity": "45"},
    {"station": "South Bay", "temperature": "101", "humidity": "38"},
    {"station": "north hill", "temperature": "75", "humidity": "50"},
    {"station": "East Ridge", "temperature": "not_a_number", "humidity": "60"},
    {"station": "West Point", "temperature": "68", "humidity": "N/A"},
    {"station": "Lake View", "temperature": "95", "humidity": "42"},
    {"station": "  Hilltop  ", "temperature": "59", "humidity": "70"},
]
```

- Row 3 (`north hill`) is the same station as row 1 (`North Hill`) once whitespace and case are normalized — it's a **duplicate**, kept as the *first* occurrence (row 1), dropped otherwise. Dropped duplicates are not errors.
- Row 4 (`East Ridge`) has an unparseable temperature (`"not_a_number"`) — this row is **dropped**, because temperature is the primary reading this pipeline exists to validate.
- Row 5 (`West Point`) has an unparseable humidity (`"N/A"`) — this row is **kept**, with humidity **filled with the column mean** of the remaining valid rows, because humidity is a secondary reading.

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | Build a `pd.DataFrame` from `raw_rows`. | 1 |
| R2 | The `station` column is cleaned with `.str.strip()` and `.str.lower()`. | 1 |
| R3 | `temperature` and `humidity` are converted with `pd.to_numeric(..., errors="coerce")` so unparseable values become `NaN` instead of crashing the script. | 1 |
| R4 | Duplicate stations (same cleaned name) are removed with `drop_duplicates(subset=["station"], keep="first")`. | 1 |
| R5 | Rows with a missing (`NaN`) `temperature` are dropped — documented reason: temperature is the primary reading. | 1 |
| R6 | Rows with a missing `humidity` are **not** dropped — instead, `humidity` is filled with `df["humidity"].mean()` — documented reason: humidity is a secondary reading. | 1 |
| R7 | A `status` column is added via `.apply()` with a `lambda`: `"ALERT"` if `temperature > 90`, else `"OK"`. | 1 |
| R8 | A `flag` column is added via `np.where()`: `"DRY"` if `humidity < 40`, else `"NORMAL"`. | 1 |
| R9 | Loading a CSV (`sensor_readings.csv`, which does not exist) is attempted inside a `try/except FileNotFoundError`, printing a clear message instead of crashing. | 1 |
| R10 | `isna().sum()` for `temperature` and `humidity` is printed **before** and **after** the cleaning steps (duplicates, drop, fill). | 1 |

## Suggested Build Order

Your script must stay runnable after every milestone.

- **M1 — Load and inspect.** Build the DataFrame. Print `df.isna().sum()` for `temperature`/`humidity` *before* any cleaning (after converting with `to_numeric`, but before dropping/filling anything).
- **M2 — Strings.** Clean the `station` column with `.str.strip().str.lower()`. Print the DataFrame.
- **M3 — Duplicates and missing values.** Drop duplicate stations, drop rows with missing temperature, fill missing humidity with the column mean. Print `df.isna().sum()` again — it should now be all zeros.
- **M4 — Derived columns.** Add `status` and `flag`. Print the full cleaned table.
- **M5 — Filtering and error handling.** Print only the `ALERT` rows using boolean filtering. Add the `try/except FileNotFoundError` demo.

## Your Task

Write a Python module named **`sensor_cleaner.py`** with:

- `clean_readings(rows)` → returns `(cleaned_df, missing_before, missing_after)`, where `missing_before`/`missing_after` are the `isna().sum()` Series described above.

## Libraries

```python
import pandas as pd
import numpy as np
```

You're welcome to use any other standard-library module if it genuinely helps. No sklearn for this remedial set.

## What You Need to Print

Running your script should print, in order:

1. Missing-value counts for `temperature` and `humidity` **before** cleaning.
2. Missing-value counts for `temperature` and `humidity` **after** cleaning (should be 0 for both).
3. The full cleaned table (station, temperature, humidity, status, flag).
4. The `FileNotFoundError` demo message from attempting to load `sensor_readings.csv`.

## Where to Review

- Building a DataFrame, `.str` methods: Week 3 Reading Guide, Chapter 3 (§3.1) and Chapter 4 (§4.5).
- `pd.to_numeric(errors="coerce")`: Week 3 Reading Guide, Chapter 4 (§4.4).
- `isna()`, `dropna()`, `fillna()`, `drop_duplicates()`: Week 3 Reading Guide, Chapter 4 (§4.1–§4.3).
- `.apply()` with `lambda`, `np.where()`: Week 3 Reading Guide, Chapter 4 (§4.7) and Chapter 2 (§2.7).
- Catching `FileNotFoundError` specifically: Week 3 Reading Guide, §3.2; Week 2 Reading Guide, Chapter 5 (§5.3).

## Submission

Work in VS Code. 

- `sensor_cleaner.py` — your complete, runnable solution.
- `writeup.md` — at least 50 words explaining your two missing-value decisions (why drop for temperature, why fill for humidity) and why they count as "documented," not arbitrary.

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

## Before You Submit

- [ ] Runs top to bottom without errors (`python sensor_cleaner.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] The "after" missing-value counts are actually 0 for both columns.
- [ ] The duplicate `north hill` row does not appear twice in your final output.
- [ ] `writeup.md` is at least 50 words and names both missing-value decisions.
