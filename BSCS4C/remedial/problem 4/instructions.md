# Remedial Problem 4: Support Ticket Triage

## Scenario

Your helpdesk exports raw support tickets as plain text lines: `id|priority|tags`. The export is manually typed by support staff, so some lines are malformed — an unrecognized priority, or a missing field entirely. You need to parse what you can, skip what you can't, and summarize the rest — without ever crashing on one bad line.

## Data

Use this raw dataset exactly as given:

```python
raw_lines = [
    "T001|high|login,auth",
    "T002|medium|billing",
    "T003|low|ui,cosmetic",
    "T004|urgent|payments",
    "T005|high|login,payments",
    "T006|medium",
    "T007|low|ui,auth,login",
]
```

- Line 4 (`T004`) uses priority `"urgent"`, which is not a valid priority (`low`, `medium`, `high` only) — **rejected**.
- Line 6 (`T006`) is missing the tags field entirely (only 2 parts instead of 3) — **rejected**.

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | `TicketFormatError(Exception)` is defined and used for every rejection below. | 1 |
| R2 | `parse_ticket_line(line)` splits on the line between each column (e.g. between T005 and high) and raises `TicketFormatError` if it doesn't get exactly 3 parts. | 1 |
| R3 | `parse_ticket_line(line)` raises `TicketFormatError` if the priority (lowercased) isn't one of `{"low", "medium", "high"}`. | 1 |
| R4 | Tags are parsed into a **set** of lowercased, stripped strings (not a list). | 1 |
| R5 | `parse_ticket_line` is decorated with a logging decorator that you write yourself, which uses `functools.wraps` so the wrapped function keeps its real `__name__`. | 2 |
| R6 | `clean_tickets(lines)` is a **generator** (uses `yield`) that lazily yields cleaned ticket dicts, printing a skip message for each malformed line instead of crashing. | 2 |
| R7 | The main flow uses a full `try/except/else/finally` around consuming the generator. | 1 |
| R8 | `count_by_priority(tickets)` builds its counts using a dict and `.get()` (not `collections.Counter`). | 1 |

## Suggested Build Order

Your script must stay runnable after every milestone.

- **M1 — Parsing one line.** Write `TicketFormatError` and `parse_ticket_line(line)` with both validation rules. Print the result of parsing one good line, and print the caught error for one bad line.
- **M2 — The decorator.** Write a decorator (using `functools.wraps`) that logs before/after each call, and apply it to `parse_ticket_line`. Print `parse_ticket_line.__name__` to prove it's still `"parse_ticket_line"`, not `"wrapper"`.
- **M3 — The generator.** Write `clean_tickets(lines)` as a generator over the full dataset. Wrap the consuming loop in `try/except/else/finally`. Print how many tickets were successfully processed.
- **M4 — Summaries.** Add `count_by_priority` and a set-based tag lookup (tickets tagged `login` or `payments`). Print both.

## Your Task

Write a Python module named **`ticket_triage.py`** with:

- `TicketFormatError(Exception)`
- a decorator (any name you choose) that logs calls via the `logging` module and uses `functools.wraps`
- `parse_ticket_line(line)` — decorated with the above
- `clean_tickets(lines)` — a generator
- `count_by_priority(tickets)` — returns a dict built with `.get()`

## Libraries

Standard library only: `logging`, `functools.wraps`. No Pandas, no NumPy, no sklearn needed — you're welcome to use other standard-library modules if it genuinely helps.

## What You Need to Print

Running your script should print, in order:

1. One line per skipped line: `Skipped line: 'T004|urgent|payments' -> reason: {error}`.
2. `"Processed 5 valid tickets."` followed by `"Triage pass complete."` (from your `try/except/else/finally`).
3. The dict from `count_by_priority(tickets)`.
4. The sorted list of ticket IDs tagged `login` or `payments`, found using a **set** intersection.

## Where to Review

- Decorators, closures, `functools.wraps`: Week 2 Reading Guide, Chapter 4 (§4.3).
- Generators and `yield`: Week 2 Reading Guide, Chapter 4 (§4.5).
- `try/except/else/finally`, custom exceptions: Week 2 Reading Guide, Chapter 5 (§5.2, §5.5).
- The `logging` module: Week 2 Reading Guide, Chapter 5 (§5.10).
- Sets, dict comprehensions, `.get()`: Week 1 Reading Guide (data structures chapter).

## Submission

Work in VS Code. 

- `ticket_triage.py` — your complete, runnable solution.
- `writeup.md` — at least 50 words on why you chose a generator for `clean_tickets` instead of returning a list, and what counts as a "malformed" line in your solution.

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

## Before You Submit

- [ ] Runs top to bottom without errors (`python ticket_triage.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] `clean_tickets` actually uses `yield`, not `return [...]`.
- [ ] `parse_ticket_line.__name__` still prints `"parse_ticket_line"`, proving `functools.wraps` is used.
- [ ] `writeup.md` is at least 50 words.
