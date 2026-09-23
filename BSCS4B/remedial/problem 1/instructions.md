# Remedial Problem 1: Library Book Catalog Validator

## Scenario

You're building the backend for a small library's catalog tool. New titles arrive as a list of raw dicts, but some entries have bad data — an impossible publication year, or a negative number of copies. Your job is to turn each valid row into a `Book` object, reject the bad ones with a clear reason, and rank what's left by copies available.

## Data

Use this raw dataset exactly as given:

```python
raw_rows = [
    {"title": "The Pragmatic Coder", "year": 2015, "copies": 6},
    {"title": "Data Structures 101", "year": 2010, "copies": 3},
    {"title": "Ghost Protocols", "year": 3050, "copies": 4},
    {"title": "Legacy Systems", "year": 2001, "copies": -1},
    {"title": "Untitled Draft", "year": 1300, "copies": 2},
    {"title": "Clean Interfaces", "year": 2019, "copies": 0},
    {"title": "Algorithms Illustrated", "year": 2022, "copies": 9},
]
```

- Row 3 (`Ghost Protocols`) has year `3050` — invalid (must be between 1450 and 2026).
- Row 4 (`Legacy Systems`) has `copies = -1` — invalid.
- Row 5 (`Untitled Draft`) has year `1300` — invalid (before the printing-press era this catalog covers).
- Row 6 (`Clean Interfaces`) has `copies = 0` — this is **valid** (zero copies on hand is not an error, it just can't be checked out right now).

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | `year` and `copies` are validated through `@property` setters at construction time. A year outside 1450–2026, or a `copies` value that is not a non-negative integer, is rejected. | 2 |
| R2 | There is a custom exception hierarchy: `CatalogError` (base), with `InvalidYearError` and `InvalidCopiesError` as subclasses. Each carries enough information (at minimum, the book title and the bad value) for the caller to understand what went wrong. | 1 |
| R3 | `checkout(n)` reduces `copies` by `n`. If `n` is more than the current copies, it raises `InvalidCopiesError` with a message explaining the shortfall — it does not silently go negative. | 1 |
| R4 | `__str__` returns one human-readable line, e.g. `The Pragmatic Coder (2015): 6 copies available`. | 1 |
| R5 | `__repr__` returns an unambiguous, constructor-like string, e.g. `Book(title='The Pragmatic Coder', year=2015, copies=6)`. | 1 |
| R6 | `__eq__` compares two `Book` objects by title, year, and copies. | 1 |
| R7 | `Book.from_dict(d)` is a `@classmethod` alternative constructor that builds a `Book` from a raw dict with keys `title`, `year`, `copies`. | 1 |
| R8 | `build_catalog(raw_rows)` returns `(books, failures)`. It builds a `Book` per row using `from_dict`, catches `CatalogError` specifically (never a bare `except:`), and never crashes on one bad row. `failures` is a list of `{"row": <original dict>, "error": <reason>}`. | 1 |
| R9 | `rank_by_availability(books)` uses `sorted()` with a `lambda` key to sort books by `copies`, descending. | 1 |

## Suggested Build Order

Work through these milestones in order. **After every milestone, your script should still run without crashing.** A runnable M1–M3 earns more partial credit than an unrunnable M1–M5.

- **M1 — Validation.** Write `CatalogError`, `InvalidYearError`, `InvalidCopiesError`, and a `Book` class with `__init__` and `@property` validation for `year` and `copies`. Print: build one valid `Book`, then attempt to build one with a bad year inside a `try/except InvalidYearError`, printing the caught error message.
- **M2 — Checkout.** Add `checkout(n)`. Print: build a book, call `checkout()` with a valid amount, then call it again with too many copies and print the caught `InvalidCopiesError`.
- **M3 — Readable objects.** Add `__str__`, `__repr__`, `__eq__`, and `from_dict`. Print: `print(book)`, `print(repr(book))`, and whether two books built from equal dicts compare equal.
- **M4 — Batch building.** Add `build_catalog(raw_rows)` using the dataset above. Print each successful book, then one line per failed row.
- **M5 — Ranking.** Add `rank_by_availability()`. Print the final ranked list in the required format.

## Your Task

Write a Python module named **`library_catalog.py`** that defines:

- `CatalogError(Exception)`, `InvalidYearError(CatalogError)`, `InvalidCopiesError(CatalogError)`
- `class Book` with `__init__(self, title, year, copies)`, `@property`/`@year.setter` for `year`, `@property`/`@copies.setter` for `copies`, `checkout(self, n)`, `__str__`, `__repr__`, `__eq__`, and `@classmethod from_dict(cls, d)`
- `build_catalog(raw_rows)` → `(books, failures)`
- `rank_by_availability(books)` → a new sorted list

## Libraries

Standard library only — this problem is pure OOP and doesn't need Pandas or NumPy. You're welcome to use any standard-library module if it genuinely helps, but no Pandas/NumPy/sklearn is required or expected here.

## What You Need to Print

Running your script should print, in order:

1. Each successfully built book via `print(book)`.
2. One line per failed row (in the order they appear in `raw_rows`): `Skipped row: {original raw dict} -> reason: {error}`.
3. One manual demonstration: build a `Book` with a small `copies` count, call `.checkout()` with more than it has, catch your custom exception, and print it.
4. The ranked list, one line per book: `1. Algorithms Illustrated — 9 copies`.

## Where to Review

- Custom exceptions, hierarchies, and `@property`: Week 2 Reading Guide, Chapter 3 (§3.3, §3.5) and Chapter 5 (§5.1, §5.5).
- `__str__`, `__repr__`, `__eq__`: Week 2 Reading Guide, Chapter 3 (§3.1, §3.4).
- `@classmethod`: Week 2 Reading Guide, Chapter 3 (§3.2).
- `sorted()` with a `lambda` key: Week 3 Reading Guide, Chapter 1 (§1.2).
- Catching specific exceptions instead of a bare `except:`: Week 2 Reading Guide, Chapter 5 (§5.3).

## Submission

Work in VS Code.

- `library_catalog.py` — your complete, runnable solution, including a `__main__` block producing everything above.
- `writeup.md` — at least 50 words on how you structured `build_catalog`, and what you decided counts as a "failure."

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

## Before You Submit

- [ ] Runs top to bottom without errors (`python library_catalog.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] All 4 print sections appear, in order, in the exact formats shown above.
- [ ] Your custom exceptions carry the book title and the bad value, not just a generic message.
- [ ] `writeup.md` is at least 50 words and actually describes your `build_catalog` logic.
