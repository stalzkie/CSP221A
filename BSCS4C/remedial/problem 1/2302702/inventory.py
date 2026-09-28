class InventoryError(Exception):
    def __init__(self, message, name, bad_value):
        super().__init__(message)
        self.name = name
        self.bad_value = bad_value


class InvalidPriceError(InventoryError):
    pass


class InvalidQuantityError(InventoryError):
    pass


class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise InvalidPriceError(f"Price must be > 0, got {value}", self.name, value)
        self._price = float(value)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise InvalidQuantityError(
                f"Quantity must be a non-negative integer, got {value}", self.name, value
            )
        self._quantity = value

    def sell(self, n: int):
        if not isinstance(n, int) or isinstance(n, bool) or n < 0 or n > self.quantity:
            raise InvalidQuantityError(
                f"Cannot sell {n} units; only {self.quantity} in stock.", self.name, n
            )
        self.quantity -= n

    def __str__(self):
        return f"{self.name}: ${self.price:.2f} x {self.quantity} in stock."

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return (self.name, self.price, self.quantity) == (other.name, other.price, other.quantity)

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d["name"], d["price"], d["quantity"])


def build_inventory(raw_rows: list[dict]):
    products = []
    failures = []
    for row in raw_rows:
        try:
            products.append(Product.from_dict(row))
        except InventoryError as e:
            failures.append({"row": row, "error": str(e)})
        except (KeyError, TypeError) as e:
            failures.append({"row": row, "error": f"Invalid product data: {e}"})
    return products, failures


def rank_by_value(products: list[Product]):
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
    for product in products:
        print(product)

    print("Skipped Rows")
    for failure in failures:
        print(f"Skipped row: {failure['row']} -> reason: {failure['error']}")

    print("Demonstration of sell Exception")
    demo_product = Product("DemoItem", 10.0, 3)
    try:
        demo_product.sell(5)
    except InvalidQuantityError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Ranked Products by Total Stock Value ---")
    ranked = rank_by_value(products)
    for i, p in enumerate(ranked, 1):
        value = p.price * p.quantity
        print(f"{i}. {p.name} — ${value:.2f} stock value")