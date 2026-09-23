# Remedial Problem 3: Warehouse Robot Battery Cycle Tracker

## Scenario

A warehouse runs a small fleet of picking robots, each logging its charge-cycle duration (in minutes) every shift. The raw log is a list of dicts, but a couple of robots have incomplete data — one was pulled for maintenance mid-shift (too few cycles logged), one never logged anything. You need to build a tracker that skips the bad entries, then use vectorized NumPy math (no loops over robots) to compute averages and flag slow charge cycles.

## Data

Use this raw dataset exactly as given:

```python
raw_rows = [
    {"robot": "R-01", "cycles": [42.0, 45.5, 41.2]},
    {"robot": "R-02", "cycles": [50.1, 48.7, 49.9]},
    {"robot": "R-03", "cycles": [39.0, 40.1]},
    {"robot": "R-04", "cycles": []},
    {"robot": "R-05", "cycles": [44.4, 43.8, 45.0]},
    {"robot": "R-06", "cycles": [55.2, 54.8, 56.1]},
]
```

- `R-03` has only 2 recorded cycles instead of the expected 3 — **rejected** as a count mismatch.
- `R-04` has no recorded cycles at all — **rejected** as an empty log.

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | `CycleCountMismatchError(Exception)` and `EmptyCycleLogError(Exception)` are both defined. | 1 |
| R2 | `build_tracker(rows, expected_cycles=3)` raises (and catches) `EmptyCycleLogError` for any robot with zero cycles, without crashing the batch. | 1 |
| R3 | `build_tracker` raises (and catches) `CycleCountMismatchError` for any robot whose cycle count doesn't match `expected_cycles`, without crashing the batch. | 1 |
| R4 | `build_tracker` returns `(tracker, failures)`, where `failures` is a list of `{"row": <original dict>, "error": <reason>}`. | 1 |
| R5 | `class BatteryCycleTracker` stores robot IDs and cycle minutes as a 2D NumPy array. | 1 |
| R6 | `BatteryCycleTracker` implements `__len__` (number of robots) and `__repr__`, e.g. `BatteryCycleTracker(n_robots=4, n_cycles=3)`. | 1 |
| R7 | `average_cycle_time()` computes each robot's average cycle time with a **vectorized** call (`self.cycles.mean(axis=1)`) — no Python loop over rows. | 2 |
| R8 | `flag_long_cycles(threshold)` uses `np.where()` to label every cycle `"SLOW_CHARGE"` or `"NORMAL"` in one vectorized call. | 1 |
| R9 | `normalize_columns()` uses broadcasting — `(self.cycles - self.cycles.mean(axis=0)) / self.cycles.std(axis=0)` — to z-score each cycle column across all robots. | 1 |

## Suggested Build Order

Your script must stay runnable after every milestone.

- **M1 — Validation errors.** Write `CycleCountMismatchError`, `EmptyCycleLogError`, and a `build_tracker` that just validates each row and prints a skip message for bad ones (don't build the array yet).
- **M2 — The tracker class.** Write `BatteryCycleTracker.__init__`, `__len__`, `__repr__`. Finish `build_tracker` so it returns `(tracker, failures)`. Print `repr(tracker)` and every skipped row.
- **M3 — Vectorized averages.** Add `average_cycle_time()`. Print each robot's average cycle time.
- **M4 — Flags and normalization.** Add `flag_long_cycles()` and `normalize_columns()`. Print the SLOW_CHARGE/NORMAL flags per robot.

## Your Task

Write a Python module named **`battery_cycle_tracker.py`** with:

- `CycleCountMismatchError(Exception)`, `EmptyCycleLogError(Exception)`
- `class BatteryCycleTracker` with `__init__(self, robot_ids, cycle_minutes)`, `__len__`, `__repr__`, `average_cycle_time(self)`, `longest_cycle(self)`, `flag_long_cycles(self, threshold)`, `normalize_columns(self)`
- `build_tracker(rows, expected_cycles=3)` → `(BatteryCycleTracker, failures)`

## Libraries

```python
import numpy as np
```

No Pandas, no sklearn needed for this problem. You're welcome to use standard-library modules if it genuinely helps.

## What You Need to Print

Running your script should print, in order:

1. `repr(tracker)`.
2. One line per skipped row: `Skipped row: {original raw dict} -> reason: {error}`.
3. Each robot's average cycle time: `R-01: 42.90 min average`.
4. Each robot's SLOW_CHARGE/NORMAL flags (threshold 45.0): `R-01: NORMAL, SLOW_CHARGE, NORMAL`.

## Where to Review

- NumPy arrays, broadcasting, vectorized math, `np.where`: Week 3 Reading Guide, Chapter 2 (all sections).
- Custom exceptions, `__len__`, `__repr__`: Week 2 Reading Guide, Chapter 3 (§3.1) and Chapter 5 (§5.5).
- Catching specific exceptions inside a batch-building loop without crashing: Week 2 Reading Guide, Chapter 5 (§5.3).

## Submission

Work in VS Code. 

- `battery_cycle_tracker.py` — your complete, runnable solution.
- `writeup.md` — at least 50 words explaining why your averages/flags count as "vectorized," and what would break that if you weren't careful.

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

## Before You Submit

- [ ] Runs top to bottom without errors (`python battery_cycle_tracker.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] `average_cycle_time()` and `flag_long_cycles()` contain no `for` loop over rows/robots.
- [ ] Both custom exceptions are actually raised and caught somewhere in `build_tracker`.
- [ ] `writeup.md` is at least 50 words.
