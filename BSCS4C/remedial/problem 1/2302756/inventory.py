class InventoryError(Exception):
    pass


class InvalidPriceError(InventoryError):
    def __init__(self, product_name, bad_value):
        self.product_name = product_name
        self.bad_value = bad_value
        super().__init__(f"'{product_name}' has invalid price: {bad_value} (must be a number > 0)")


class InvalidQuantityError(InventoryError):
    def __init__(self, product_name, bad_value, details="Quantity must be an integer >= 0"):
        self.product_name = product_name
        self.bad_value = bad_value
        super().__init__(f"'{product_name}' quantity error ({bad_value}): {details}")


class Product:
    def __init__(self, name, price, quantity):
        self.name = str(name)
        self.price = price
        self.quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, amount):
        if type(amount) not in (int, float) or amount <= 0:
            raise InvalidPriceError(getattr(self, "name", "Product"), amount)
        self._price = float(amount)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, count):
        if type(count) is not int or count < 0:
            raise InvalidQuantityError(getattr(self, "name", "Product"), count)
        self._quantity = count

    def sell(self, count):
        if type(count) is not int or count <= 0:
            raise InvalidQuantityError(self.name, count, "Sale amount must be positive integer")
        if count > self._quantity:
            shortage = count - self._quantity
            raise InvalidQuantityError(self.name, count, f"Not enough stock to sell {count} (missing {shortage})")
        self._quantity -= count

    def __str__(self):
        return f"{self.name}: ${self.price:.2f} x {self.quantity} in stock"

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return (self.name, self.price, self.quantity) == (other.name, other.price, other.quantity)

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["price"], data["quantity"])


def build_inventory(raw_rows):
    valid_list = []
    error_list = []

    for entry in raw_rows:
        try:
            valid_list.append(Product.from_dict(entry))
        except InventoryError as err:
            error_list.append({"row": entry, "error": str(err)})

    return valid_list, error_list


def rank_by_value(products):
    return sorted(products, key=lambda item: item.price * item.quantity, reverse=True)


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

    stock, errors = build_inventory(raw_rows)

    for item in stock:
        print(item)

    for failed in errors:
        print(f"Skipped row: {failed['row']} -> reason: {failed['error']}")

    test_item = Product("DemoItem", 10.0, 3)
    try:
        test_item.sell(5)
    except InvalidQuantityError as exc:
        print(f"Caught expected error: {exc}")

    ranked_stock = rank_by_value(stock)
    for rank, item in enumerate(ranked_stock, start=1):
        total_val = item.price * item.quantity
        print(f"{rank}. {item.name} — ${total_val:.2f} stock value")