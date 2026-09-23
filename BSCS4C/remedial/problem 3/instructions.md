# Remedial Problem 3: Fitness Challenge Lap Tracker

## Scenario

A local fitness challenge tracks each athlete's lap times over a 3-lap sprint. The raw sign-up sheet is a list of dicts, but a couple of athletes have incomplete data — one dropped out early (too few laps recorded), one never started (no laps at all). You need to build a tracker that skips the bad entries, then use vectorized NumPy math (no loops over athletes) to compute averages and flag slow laps.

## Data

Use this raw dataset exactly as given:

```python
raw_rows = [
    {"athlete": "Ava", "laps": [61.2, 60.8, 62.1]},
    {"athlete": "Ben", "laps": [58.5, 59.0, 57.9]},
    {"athlete": "Cleo", "laps": [65.0, 64.2]},
    {"athlete": "Drew", "laps": []},
    {"athlete": "Elle", "laps": [60.1, 59.8, 60.5]},
    {"athlete": "Finn", "laps": [63.3, 62.9, 63.7]},
]
```

- `Cleo` has only 2 recorded lap times instead of the expected 3 — **rejected** as a shape mismatch.
- `Drew` has no recorded lap times at all — **rejected** as an empty log.

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | `ShapeMismatchError(Exception)` and `EmptyLapsError(Exception)` are both defined. | 1 |
| R2 | `build_tracker(rows, expected_laps=3)` raises (and catches) `EmptyLapsError` for any athlete with zero laps, without crashing the batch. | 1 |
| R3 | `build_tracker` raises (and catches) `ShapeMismatchError` for any athlete whose lap count doesn't match `expected_laps`, without crashing the batch. | 1 |
| R4 | `build_tracker` returns `(tracker, failures)`, where `failures` is a list of `{"row": <original dict>, "error": <reason>}`. | 1 |
| R5 | `class LapTimeTracker` stores athlete names and lap times as a 2D NumPy array. | 1 |
| R6 | `LapTimeTracker` implements `__len__` (number of athletes) and `__repr__`, e.g. `LapTimeTracker(n_athletes=4, n_laps=3)`. | 1 |
| R7 | `average_times()` computes each athlete's average lap time with a **vectorized** call (`self.times.mean(axis=1)`) — no Python loop over rows. | 2 |
| R8 | `flag_slow_laps(threshold)` uses `np.where()` to label every lap `"SLOW"` or `"FAST"` in one vectorized call. | 1 |
| R9 | `normalize_columns()` uses broadcasting — `(self.times - self.times.mean(axis=0)) / self.times.std(axis=0)` — to z-score each lap column across all athletes. | 1 |

## Suggested Build Order

Your script must stay runnable after every milestone.

- **M1 — Validation errors.** Write `ShapeMismatchError`, `EmptyLapsError`, and a `build_tracker` that just validates each row and prints a skip message for bad ones (don't build the array yet).
- **M2 — The tracker class.** Write `LapTimeTracker.__init__`, `__len__`, `__repr__`. Finish `build_tracker` so it returns `(tracker, failures)`. Print `repr(tracker)` and every skipped row.
- **M3 — Vectorized averages.** Add `average_times()`. Print each athlete's average lap time.
- **M4 — Flags and normalization.** Add `flag_slow_laps()` and `normalize_columns()`. Print the SLOW/FAST flags per athlete.

## Your Task

Write a Python module named **`lap_time_tracker.py`** with:

- `ShapeMismatchError(Exception)`, `EmptyLapsError(Exception)`
- `class LapTimeTracker` with `__init__(self, names, lap_times)`, `__len__`, `__repr__`, `average_times(self)`, `fastest_lap_per_athlete(self)`, `flag_slow_laps(self, threshold)`, `normalize_columns(self)`
- `build_tracker(rows, expected_laps=3)` → `(LapTimeTracker, failures)`

## Libraries

```python
import numpy as np
```

No Pandas, no sklearn needed for this problem. You're welcome to use standard-library modules if it genuinely helps.

## What You Need to Print

Running your script should print, in order:

1. `repr(tracker)`.
2. One line per skipped row: `Skipped row: {original raw dict} -> reason: {error}`.
3. Each athlete's average lap time: `Ava: 61.37s average`.
4. Each athlete's SLOW/FAST flags (threshold 61.0): `Ava: SLOW, FAST, SLOW`.

## Where to Review

- NumPy arrays, broadcasting, vectorized math, `np.where`: Week 3 Reading Guide, Chapter 2 (all sections).
- Custom exceptions, `__len__`, `__repr__`: Week 2 Reading Guide, Chapter 3 (§3.1) and Chapter 5 (§5.5).
- Catching specific exceptions inside a batch-building loop without crashing: Week 2 Reading Guide, Chapter 5 (§5.3).

## Submission

Work in VS Code. 

- `lap_time_tracker.py` — your complete, runnable solution.
- `writeup.md` — at least 50 words explaining why your averages/flags count as "vectorized," and what would break that if you weren't careful.

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

**Deadline:** `[INSTRUCTOR TO FILL IN]`
**Late policy:** `[INSTRUCTOR TO FILL IN]`

## Before You Submit

- [ ] Runs top to bottom without errors (`python lap_time_tracker.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] `average_times()` and `flag_slow_laps()` contain no `for` loop over rows/athletes.
- [ ] Both custom exceptions are actually raised and caught somewhere in `build_tracker`.
- [ ] `writeup.md` is at least 50 words.
