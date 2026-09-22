class InventoryError(Exception):
    def __init__(self, message, name):
        super().__init__(message)
        self.name = name
        
class InvalidPriceError(InventoryError):
    def __init__(self, name, price):
        message = f"Invalid Price of [{name}]. Price $[{price}] must be greater than zero."
        super().__init__(message, name)
        self.price = price

class InvalidQuantityError(InventoryError):
    def __init__(self, name, quantity):
        message = f"Invalid Quantity of [{name}]. Quantity [{quantity}] cannot be negative (or purchase quantity exceeds stock)."
        super().__init__(message, name)
        self.quantity = quantity

class Product:
    def __init__(self, name, price=1, quantity=1):
        self.name = name
        self.price = price
        self.quantity = quantity
        
    @classmethod
    def from_dict(cls, d):
        return cls(**d)
    
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
    
    def __str__(self):
        return f"{self.name}: ${self.price:.2f} x {self.quantity} in stock"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, price={self.price!r}, quantity={self.quantity!r})"
    
    def __eq__(self, other):
        return (self.name, self.price, self.quantity) == (other.name, other.price, other.quantity)
    
    def sell(self, n):
        if n > self.quantity:
            raise InvalidQuantityError(self.name, self.quantity)
        else:
            self.quantity = self.quantity - n
    
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
    return sorted(products, key=lambda s: (s.price * s.quantity), reverse=True)
   
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
    
    for product in products:
        print(product)
        
    for failure in failures:
        print(f"Skipped row: {failure['row']} -> reason: {failure['error']}")
    
    new_product = Product("Mouse", 20, 5)
    try:
        new_product.sell(10)
    except InvalidQuantityError as e:
        print(e)
        
    ranked_products = rank_by_value(products)
    count = 1
    for rank in ranked_products:
        total_value = rank.price * rank.quantity
        print(f"{count}. {rank.name} — ${total_value:.2f} stock value")
        count += 1