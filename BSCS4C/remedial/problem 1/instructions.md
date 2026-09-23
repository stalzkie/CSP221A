# Remedial Problem 1: Product Inventory Validator

## Scenario

You're building the backend for a small hardware shop's inventory tracker. New stock arrives as a list of raw dicts from a spreadsheet export, and some of those rows have bad data — a negative price, a negative quantity, or a price of zero. Your job is to turn each valid row into a `Product` object, reject the bad ones with a clear reason, and rank what's left by total stock value.

## Data

Use this raw dataset exactly as given:

```python
raw_rows = [
    {"name": "Widget", "price": 12.50, "quantity": 40},
    {"name": "Gadget", "price": 8.00, "quantity": 15},
    {"name": "Gizmo", "price": -5.00, "quantity": 10},
    {"name": "Doohickey", "price": 3.25, "quantity": -2},
    {"name": "Thingamajig", "price": 0, "quantity": 5},
    {"name": "Contraption", "price": 15.00, "quantity": 0},
    {"name": "Sprocket", "price": 6.75, "quantity": 25},
]
```

- Row 3 (`Gizmo`) has a negative price — invalid.
- Row 4 (`Doohickey`) has a negative quantity — invalid.
- Row 5 (`Thingamajig`) has a price of exactly 0 — invalid (price must be **greater than** 0).
- Row 6 (`Contraption`) has a quantity of exactly 0 — this is **valid** (zero stock is not an error, it just can't be sold).

## Rules (10 points total)

| # | Rule | Points |
|---|------|--------|
| R1 | `price` and `quantity` are validated through `@property` setters at construction time. A price that is not a number greater than 0, or a quantity that is not a non-negative integer, is rejected. | 2 |
| R2 | There is a custom exception hierarchy: `InventoryError` (base), with `InvalidPriceError` and `InvalidQuantityError` as subclasses. Each carries enough information (at minimum, the product name and the bad value) for the caller to understand what went wrong. | 1 |
| R3 | `sell(n)` reduces `quantity` by `n`. If `n` is more than the current quantity, it raises `InvalidQuantityError` with a message explaining the shortfall — it does not silently go negative. | 1 |
| R4 | `__str__` returns one human-readable line, e.g. `Widget: $12.50 x 40 in stock`. | 1 |
| R5 | `__repr__` returns an unambiguous, constructor-like string, e.g. `Product(name='Widget', price=12.5, quantity=40)`. | 1 |
| R6 | `__eq__` compares two `Product` objects by name, price, and quantity. | 1 |
| R7 | `Product.from_dict(d)` is a `@classmethod` alternative constructor that builds a `Product` from a raw dict with keys `name`, `price`, `quantity`. | 1 |
| R8 | `build_inventory(raw_rows)` returns `(products, failures)`. It builds a `Product` per row using `from_dict`, catches `InventoryError` specifically (never a bare `except:`), and never crashes on one bad row. `failures` is a list of `{"row": <original dict>, "error": <reason>}`. | 1 |
| R9 | `rank_by_value(products)` uses `sorted()` with a `lambda` key to sort products by `price * quantity`, descending. | 1 |

## Suggested Build Order

Work through these milestones in order. **After every milestone, your script should still run without crashing.** A runnable M1–M3 earns more partial credit than an unrunnable M1–M5, so don't skip ahead if something is broken.

- **M1 — Validation.** Write `InventoryError`, `InvalidPriceError`, `InvalidQuantityError`, and a `Product` class with `__init__` and `@property` validation for `price` and `quantity`. Print: build one valid `Product`, then attempt to build one with a bad price inside a `try/except InvalidPriceError`, printing the caught error message.
- **M2 — Selling.** Add `sell(n)`. Print: build a product, call `sell()` with a valid amount, then call it again with too much stock and print the caught `InvalidQuantityError`.
- **M3 — Readable objects.** Add `__str__`, `__repr__`, `__eq__`, and `from_dict`. Print: `print(product)`, `print(repr(product))`, and whether two products built from equal dicts compare equal.
- **M4 — Batch building.** Add `build_inventory(raw_rows)` using the dataset above. Print each successful product, then one line per failed row.
- **M5 — Ranking.** Add `rank_by_value()`. Print the final ranked list in the required format.

## Your Task

Write a Python module named **`inventory.py`** that defines:

- `InventoryError(Exception)`, `InvalidPriceError(InventoryError)`, `InvalidQuantityError(InventoryError)`
- `class Product` with `__init__(self, name, price, quantity)`, `@property`/`@price.setter` for `price`, `@property`/`@quantity.setter` for `quantity`, `sell(self, n)`, `__str__`, `__repr__`, `__eq__`, and `@classmethod from_dict(cls, d)`
- `build_inventory(raw_rows)` → `(products, failures)`
- `rank_by_value(products)` → a new sorted list

## Libraries

Standard library only — this problem is pure OOP and doesn't need Pandas or NumPy. You're welcome to use any standard-library module if it genuinely helps, but no Pandas/NumPy/sklearn is required or expected here.

## What You Need to Print

Running your script should print, in order:

1. Each successfully built product via `print(product)`.
2. One line per failed row (in the order they appear in `raw_rows`): `Skipped row: {original raw dict} -> reason: {error}`.
3. One manual demonstration: build a `Product` with a small quantity, call `.sell()` with more than it has, catch your custom exception, and print it.
4. The ranked list, one line per product: `1. Widget — $500.00 stock value` (value = `price * quantity`, 2 decimal places).

## Where to Review

- Custom exceptions, hierarchies, and `@property`: Week 2 Reading Guide, Chapter 3 (§3.3, §3.5) and Chapter 5 (§5.1, §5.5).
- `__str__`, `__repr__`, `__eq__`: Week 2 Reading Guide, Chapter 3 (§3.1, §3.4).
- `@classmethod`: Week 2 Reading Guide, Chapter 3 (§3.2).
- `sorted()` with a `lambda` key: Week 3 Reading Guide, Chapter 1 (§1.2).
- Catching specific exceptions instead of a bare `except:`: Week 2 Reading Guide, Chapter 5 (§5.3).

## Submission

Work in VS Code. 

- `inventory.py` — your complete, runnable solution, including a `__main__` block producing everything above.
- `writeup.md` — at least 50 words on how you structured `build_inventory`, and what you decided counts as a "failure."

**One commit** with a clear, descriptive message, pushed to your GitHub repo.

## Before You Submit

- [ ] Runs top to bottom without errors (`python inventory.py`).
- [ ] No bare `except:` anywhere in the file.
- [ ] All 4 print sections appear, in order, in the exact formats shown above.
- [ ] Your custom exceptions carry the product name and the bad value, not just a generic message.
- [ ] `writeup.md` is at least 50 words and actually describes your `build_inventory` logic.
