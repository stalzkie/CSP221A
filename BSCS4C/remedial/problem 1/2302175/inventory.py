class InventoryError(Exception):
    def __init__(self, message, name, value):
        super().__init__(message)
        self.name = name
        self.value = value


class InvalidPriceError(InventoryError):
    def __init__(self, name, value):
        message = f"The product {name} has an invalid price: {value}. Prices should be above zero."
        super().__init__(message=message, name=name, value=value)


class InvalidQuantityError(InventoryError):
    def __init__(self, name, value):
        message = f"The product {name} has an invalid quantity: {value}. The quantity of a product must not reach negative"
        super().__init__(message=message, name=name, value=value)

class Product():
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    #PRICE SHOULD NOT STORE 0 OR NEGATIVE VALUES
    @property
    def price(self): 
        return self._price
    
    @price.setter
    def price(self, value):
        if value <= 0: 
            raise InvalidPriceError(self.name, value)
        self._price = value

    #QUANTITY SHOULD NOT STORE NEGATIVE VALUES
    @property
    def quantity(self): 
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise InvalidQuantityError(self.name, value)
        self._quantity = value
    
    #SELL FUNCTION, DEDUCTS THE PRODUCT'S QUANTITY IF FUNCTION CALLED
    #SELL VALUE SHOULD NOT BE MORE THAN THE CURRENT QUANTY VALUE, MEANING SHOULD BE EXACT AMOUNT OR LOWER
    def sell(self, n):
        #CALL INVALIDQUANTITYERROR
        if n > self.quantity or n <=0:
            #needs custom message for sell
            raise InvalidQuantityError(self.name, f"(Product Quantity: {self.quantity}, Sell Quantity: {n}, leaving {self.quantity -n})")
        self.quantity -= n
        

    #FOR PRICE $
    def __str__(self):
        return f"{self.name}: ${self.price} x {self.quantity} in stock"

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price!r}, quantity={self.quantity!r})"
    
    def __eq__(self, other):
        return self.name == other.name and self.price == other.price and self.quantity == other.quantity
    

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d["price"], d["quantity"])


def build_inventory(raw_rows):
    products = []
    failures = []

    for row in raw_rows:
        try:
            product = Product.from_dict(row)
            products.append(product)
        except InventoryError as e:
            failures.append({"row": row, "error":str(e)})

    return products, failures

def rank_by_value(products):
    return sorted(products, key=lambda s: s.price * s.quantity, reverse=True)

    
raw_rows = [
    {"name": "Widget", "price": 12.50, "quantity": 40},
    {"name": "Gadget", "price": 8.00, "quantity": 15},
    {"name": "Gizmo", "price": -5.00, "quantity": 10},
    {"name": "Doohickey", "price": 3.25, "quantity": -2},
    {"name": "Thingamajig", "price": 0, "quantity": 5},
    {"name": "Contraption", "price": 15.00, "quantity": 0},
    {"name": "Sprocket", "price": 6.75, "quantity": 25},
]

if __name__ == "__main__":  
    products, failures = build_inventory(raw_rows)

    for product in products:
        print(product)

    for item in failures:
        print(f"Skipped row: {item['row']} -> reason: {item['error']}")

    try:
        sell_product = Product("Iphone", 3.55, 10)
        sell_product.sell(15)
    except InventoryError as e:
        print(e)

    ranked_products = rank_by_value(products)
    for i in range(len(ranked_products)):
        product = ranked_products[i]
        rank = i + 1
        total_value = product.price * product.quantity
        print(f"{rank}. {product.name} - ${total_value:.2f} stock value")




    
   

        
