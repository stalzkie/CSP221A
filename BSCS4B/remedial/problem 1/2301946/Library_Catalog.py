raw_rows = [
    {"title": "The Pragmatic Coder", "year": 2015, "copies": 6},
    {"title": "Data Structures 101", "year": 2010, "copies": 3},
    {"title": "Ghost Protocols", "year": 3050, "copies": 4},
    {"title": "Legacy Systems", "year": 2001, "copies": -1},
    {"title": "Untitled Draft", "year": 1300, "copies": 2},
    {"title": "Clean Interfaces", "year": 2019, "copies": 0},
    {"title": "Algorithms Illustrated", "year": 2022, "copies": 9},
]

class CatalogError(Exception):
    pass 

class InvalidYearError(CatalogError):
    def __init__(self, title, year):
        super().__init__(f"'{title}' has an Invalid year- '{year}")
        self.title=title
        self.year=year
        
class InvalidCopiesError(CatalogError):
    def __init__(self, title, copies):
        super().__init__(f"'{title}' has a invalid number of Copies: '{copies}'")
        self.title=title
        self.copies=copies

class Book:
    def __init__(self, title, year, copies):
        self.title=title
        self.year=year
        self.copies=copies
    
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if value > 2026  or value < 1450:
            raise InvalidYearError(self.title, value)
        self._year=value

    @property
    def copies(self):
        return self._copies
    
    @copies.setter
    def copies(self, copy):
        if type(copy) is not int or copy < 0:
            raise InvalidCopiesError(self.title, copy)
        self._copies=copy

    @classmethod
    def from_dict(dct, d):
        return dct(d["title"], d["year"], d["copies"])

    def __str__(self):
        return f"{self.title}({self.year}):{self.copies} copies are available"
    
    def __repr__(self):
        return f"Book(title='{self.title}', year={self.year}, copies={self.copies})"
    
    def __eq__(self, other):
        return self.title == other.title and self.year == other.year and self.copies == other.copies

    def checkout(self, n):
        if n > self.copies:
            raise InvalidCopiesError(self.title, n)
        self.copies -= n

def build_catalog(raw_rows):
    books = []
    failed = []
    for row in raw_rows:
        try:
            book = Book.from_dict(row)
            books.append(book)
        except CatalogError as E:
            failed.append({"row": row, "error": str(E)})
    return books, failed
                
def rank_by_availability(books):
        return sorted(books, key=lambda b : b.copies, reverse=True)
        

if __name__ == '__main__':
    books, failures = build_catalog(raw_rows)

    print("--Successful Books--")
    for b in books:
        print(b)
    for f in failures:
        print (f"Skipped row: {f['row']} -> reason: {f['error']}")

    print("\n--checkout demo--")
    dm_book = Book("test101", 2021, 2)
    try:
        dm_book.checkout(10)
    except InvalidCopiesError as E:
        print(E)
        
    print("\n--Catalog--")
    ranked = rank_by_availability(books)
    for ind, b in enumerate(ranked, start=1):
        print (f"{ind}. {b.title}—{b.copies} copies ")

        
        