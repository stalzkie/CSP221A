from dataclasses import dataclass
from typing import List


class InventoryError(Exception):
    pass


class InvalidPriceError(InventoryError):
    def __init__(self, name: str, price: float):
        super().__init__(f"Invalid price for {name}: {price}")


class InvalidQuantityError(InventoryError):
    def __init__(self, name: str, quantity: int, message: str = None):
        self.name = name
        self.quantity = quantity
        if message is None:
            message = f"Invalid quantity for {name}: {quantity}"
        super().__init__(message)


@dataclass
class Product:
    name: str
    price: float
    quantity: int

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise InvalidPriceError(self.name, value)
        self._price = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise InvalidQuantityError(self.name, value)
        self._quantity = value

    def sell(self, n: int):
        if n > self.quantity:
            raise InvalidQuantityError(
                self.name,
                n,
                f"Cannot sell {n} of {self.name}: only {self.quantity} in stock (short by {n - self.quantity})"
            )
        self.quantity -= n

    def __str__(self):
        return f"{self.name}: ${self.price:.2f} x {self.quantity} in stock"

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"

    def __eq__(self, other):
        return (self.name == other.name and
                self.price == other.price and
                self.quantity == other.quantity)

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d['name'], d['price'], d['quantity'])


def build_inventory(raw_rows: List[dict]) -> tuple[List[Product], List[dict]]:
    products = []
    failures = []
    for row in raw_rows:
        try:
            product = Product.from_dict(row)
            products.append(product)
        except InventoryError as e:
            failures.append({"row": row, "error": str(e)})
    return products, failures


def rank_by_value(products: List[Product]) -> List[Product]:
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

    print("Successful products:")
    for product in products:
        print(product)

    print("\nFailed rows:")
    for failure in failures:
        print(f"Skipped row: {failure['row']} -> reason: {failure['error']}")

    demo_product = Product("Bolt", 0.50, 3)
    try:
        demo_product.sell(10)
    except InvalidQuantityError as e:
        print(f"\nCaught {e}")

    ranked_products = rank_by_value(products)
    print("\nRanked products:")
    for i, product in enumerate(ranked_products):
        value = product.price * product.quantity
        print(f"{i + 1}. {product.name} \u2014 ${value:.2f} stock value")