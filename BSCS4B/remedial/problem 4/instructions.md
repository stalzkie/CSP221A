# Remedial Problem 4: Volunteer Shift Signup Parser

## Scenario

A campus volunteer event collects shift sign-ups as plain text lines: `id|shift|skills`. The sign-up sheet is filled in by hand at a table, so some lines are malformed — an unrecognized shift name, or a missing field entirely. You need to parse what you can, skip what you can't, and summarize the rest — without ever crashing on one bad line.

## Data

Use this raw dataset exactly as given:

```python
raw_lines = [
    "V001|morning|setup,registration",
    "V002|afternoon|food",
    "V003|evening|cleanup,setup",
    "V004|night|security",
    "V005|morning|registration,food",
    "V006|afternoon",
    "V007|evening|cleanup",
]
```

- Line 4 (`V004`) uses shift `"night"`, which is not a valid shift (`morning`, `afternoon`, `evening` only) — **rejected**.
- Line 6 (`V006`) is missing the skills field entirely (only 2 parts instead of 3) — **rejected**.

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | `SignupFormatError(Exception)` is defined and used for every rejection below. | 1 |
| R2 | `parse_signup_line(line)` splits on `"|"` and raises `SignupFormatError` if it doesn't get exactly 3 parts. | 1 |
| R3 | `parse_signup_line(line)` raises `SignupFormatError` if the shift (lowercased) isn't one of `{"morning", "afternoon", "evening"}`. | 1 |
| R4 | Skills are parsed into a **set** of lowercased, stripped strings (not a list). | 1 |
| R5 | `parse_signup_line` is decorated with a logging decorator that you write yourself, which uses `functools.wraps` so the wrapped function keeps its real `__name__`. | 2 |
| R6 | `clean_signups(lines)` is a **generator** (uses `yield`) that lazily yields cleaned signup dicts, printing a skip message for each malformed line instead of crashing. | 2 |
| R7 | The main flow uses a full `try/except/else/finally` around consuming the generator. | 1 |
| R8 | `count_by_shift(signups)` builds its counts using a dict and `.get()` (not `collections.Counter`). | 1 |

## Suggested Build Order

Your script must stay runnable after every milestone.

- **M1 — Parsing one line.** Write `SignupFormatError` and `parse_signup_line(line)` with both validation rules. Print the result of parsing one good line, and print the caught error for one bad line.
- **M2 — The decorator.** Write a decorator (using `functools.wraps`) that logs before/after each call, and apply it to `parse_signup_line`. Print `parse_signup_line.__name__` to prove it's still `"parse_signup_line"`, not `"wrapper"`.
- **M3 — The generator.** Write `clean_signups(lines)` as a generator over the full dataset. Wrap the consuming loop in `try/except/else/finally`. Print how many signups were successfully processed.
- **M4 — Summaries.** Add `count_by_shift` and a set-based skill lookup (volunteers with `setup` or `food` skills). Print both.

## Your Task

Write a Python module named **`volunteer_signups.py`** with:

- `SignupFormatError(Exception)`
- a decorator (any name you choose) that logs calls via the `logging` module and uses `functools.wraps`
- `parse_signup_line(line)` — decorated with the above
- `clean_signups(lines)` — a generator
- `count_by_shift(signups)` — returns a dict built with `.get()`

## Libraries

Standard library only: `logging`, `functools.wraps`. No Pandas, no NumPy, no sklearn needed — you're welcome to use other standard-library modules if it genuinely helps.

## What You Need to Print

Running your script should print, in order:

1. One line per skipped line: `Skipped line: 'V004|night|security' -> reason: {error}`.
2. `"Processed 5 valid signups."` followed by `"Signup pass complete."` (from your `try/except/else/finally`).
3. The dict from `count_by_shift(signups)`.
4. The sorted list of volunteer IDs with the `setup` or `food` skill, found using a **set** intersection.

## Where to Review

- Decorators, closures, `functools.wraps`: Week 2 Reading Guide, Chapter 4 (§4.3).
- Generators and `yield`: Week 2 Reading Guide, Chapter 4 (§4.5).
- `try/except/else/finally`, custom exceptions: Week 2 Reading Guide, Chapter 5 (§5.2, §5.5).
- The `logging` module: Week 2 Reading Guide, Chapter 5 (§5.10).
- Sets, dict comprehensions, `.get()`: Week 1 Reading Guide (data structures chapter).

## Submission

Work in VS Code. 

- `volunteer_signups.py` — your complete, runnable solution.
- `writeup.md` — at least 50 words on why you chose a generator for `clean_signups` instead of returning a list, and what counts as a "malformed" line in your solution.

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

## Before You Submit

- [ ] Runs top to bottom without errors (`python volunteer_signups.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] `clean_signups` actually uses `yield`, not `return [...]`.
- [ ] `parse_signup_line.__name__` still prints `"parse_signup_line"`, proving `functools.wraps` is used.
- [ ] `writeup.md` is at least 50 words.
