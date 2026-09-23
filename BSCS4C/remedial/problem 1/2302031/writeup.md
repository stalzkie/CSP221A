# Writeup

This is my explination, build_inventory loops through raw_rows and tries to build a Product from each one using from_dict(). 
All validation happens inside the price and quantity setters, so I just catch InventoryError, never a bare except and,sort rows 
into products or failures accordingly, keeping the original dict and error message for each failed row.
A row only fails if price isn't positive or quantity is negative. Zero quantity is valid, not a failure.