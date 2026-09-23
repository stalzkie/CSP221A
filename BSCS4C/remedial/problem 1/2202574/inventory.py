#base exception class
class InventoryError(Exception):
    pass

#custom exception classes for specific inventory errors

#when price is negativee
class InvalidPriceError(InventoryError):
    def __init__(self, name, price):
        self.name = name
        self.price = price
        super().__init__(f"Invalid product: {name} with price {price}")

# when quantity is negative or insufficient 
class InvalidQuantityError(InventoryError):
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        super().__init__(f"Invalid quantity: {quantity}")

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def name(self):
            return self._name

    @name.setter
    def name(self, value):
            self._name = value

    @property
    def price(self):
            return self._price

    @price.setter
    def price(self, value): 
     if not isinstance(value, (int, float)) or value <= 0: 
        raise InvalidPriceError(getattr(self, 'name', 'Unknown'), value)
     self._price = value

    @property 
    def quantity(self): 
        return self._quantity 

    @quantity.setter
    def quantity(self, value):
     if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise InvalidQuantityError(getattr(self, 'name', 'Unknown'), value)
     self._quantity = value


    def sell(self, n):
         if n > self.quantity:
            raise InvalidQuantityError(self.name, f"cannot sell {n} units, only {self.quantity} in stock")
         self.quantity -= n
    def __str__(self):
            return f"{self.name} ${self.price:.2f} x {self.quantity} in stock"

    def __repr__(self):
            return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"

    def __eq__(self, other):
            if not isinstance(other, Product):
                return False
            return (self.name == other.name and 
                    self.price == other.price and 
                    self.quantity == other.quantity)

    @classmethod
    def from_dict(cls, d):
        return cls(d['name'], d['price'], d['quantity'])

def build_inventory(raw_rows):
        products = []
        failures = []
        for row in raw_rows:
            try:
                product = Product.from_dict(row)
                products.append(product)
            except InventoryError as e:
                failures.append({"row": row, "error": str(e)})

        return products, failures

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

    print("Valid Products:")
    for product in products:
        print(product)
        print()

    print("Failed Rows:")
    for failure in failures:
        print(f"Skipped row: {failure['row']} -> reason: {failure['error']}")
        print()

    print("Manual Sell demo")
    demo_product = Product("DemoItem", 10.0, 5)
    print(f"Created: {demo_product}")
    print("Attempting to sell 10...")
    try:
        demo_product.sell(10)
    except InvalidQuantityError as e:
        print(f"Caught Expected Error: {e}")
    print()

    print("Inventory Ranking by value")
    ranked_products = rank_by_value(products)
    for i, product in enumerate(ranked_products, start=1):
        value = product.price * product.quantity
        print(f"{i}. {product.name} - ${value:.2f} stock value")