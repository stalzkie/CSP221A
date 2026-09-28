
#M1
class InventoryError(Exception):
  pass

class InvalidPriceError(InventoryError):
  def __init__(self, name, bad_value):
    self.name = name
    self.bad_value = bad_value
    message = f"{name}: invalid price {bad_value!r} (must be a number > 0)"
    super().__init__(message)

class InvalidQuantityError(InventoryError):
  def __init__(self, name, bad_value, reason=None):
    self.name = name
    self.bad_value = bad_value
    if reason is None:
      reason = "must be a non-negative integer"
    message = f"{name}: invalid quantity {bad_value!r} ({reason})"
    super().__init__(message)

class Product:
    def __init__(self, name, price, quantity):
      self.name = name
      self.price = price
      self.quantity = quantity

    @property
    def price(self):
      return self._price

    @price.setter
    def price(self, value):
      if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidPriceError(self.name, value)
      if value <= 0:
        raise InvalidPriceError(self.name, value)
      self._price = float(value)

    @property
    def quantity(self):
      return self._quantity

    @quantity.setter
    def quantity(self, value):
      if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidQuantityError(self.name, value)
      if value < 0:
        raise InvalidQuantityError(self.name, value)
      self._quantity = value

#M2
    def sell(self, n):
      if n > self.quantity:
        shortfall = n - self.quantity
        raise InvalidQuantityError(
          self.name, n,
            reason=f"only {self.quantity} in stock, short by {shortfall}",)
      self.quantity = self.quantity - n
#M3
    def __str__(self):
      return f"{self.name}: ${self.price:.2f} x {self.quantity} in stock"

    def __repr__(self):
      return f"Product(name={self.name!r}, price={self.price!r}, quantity={self.quantity!r})"

    def __eq__(self, other):
        if not isinstance(other, Product):
          return NotImplemented
        return (
          self.name == other.name
          and self.price == other.price
          and self.quantity == other.quantity
        )

    @classmethod
    def from_dict(cls, d):
      return cls(name=d["name"], price=d["price"], quantity=d["quantity"])

#M4
def build_inventory(raw_rows):
  products = []
  failures = []

  for row in raw_rows:
    try:
      product = Product.from_dict(row)
    except InventoryError as e:
      failures.append({"row": row, "error": str(e)})
    else:
      products.append(product)
  return products, failures
#M5
def rank_by_value(products):
  return sorted(products, key=lambda p: p.price * p.quantity, reverse=True)

if __name__ == "__main__":
    raw_rows = [
    {"name": "Widget", "price": 12.50, "quantity": 40},
    {"name": "Gadget", "price": 8.00, "quantity": 15},
    {"name": "Gizmo", "price": -5.00, "quantity": 10},
    {"name": "Doohickey", "price": 3.25, "quantity": -2},
    {"name": "Thingamajig", "price": 0, "quantity": 5},
    {"name": "Contraption", "price": 15.00, "quantity": 0},
    {"name": "Sprocket", "price": 6.75, "quantity": 25},
]

    products, failures = build_inventory(raw_rows)

    print("Successfully Built Products")
    for p in products:
      print(p)

    print("\nSkipped/Invalid Rows")
    for f in failures:
      print(f"Skipped row: {f['row']} -> reason: {f['error']}")

    print("\nInsufficient Stock")
    demo = Product("Demo Product", 1.0, 3)
    try:
      demo.sell(5)
    except InvalidQuantityError as e:
      print(e)

    print("\nProducts Ranked by Stock Value")
    ranked = rank_by_value(products)
    for i, p in enumerate(ranked, start=1):
      value = p.price * p.quantity
      print(f"{i}. {p.name} — ${value:.2f} stock value")