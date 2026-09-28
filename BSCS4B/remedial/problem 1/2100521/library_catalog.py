class CatalogError(Exception): #make a parent class for Exception handling
    pass

class InvalidYearError(CatalogError):
    def __init__(self, title, invalid_year):
        self.title = title
        self.invalid_year = invalid_year
        message = (
            f"Invalid year for '{title}': {invalid_year}. "
            "Year must be between 1450 and 2026."
        )
        super().__init__(message)

class InvalidCopiesError(CatalogError):
    def __init__(self, title, invalid_copies, reason):
        self.title = title
        self.invalid_copies = invalid_copies
        message = f"Invalid copies for '{title}': {invalid_copies}. {reason}."
        super().__init__(message)

#create book class to define the function for book
class Book: 
    def __init__(self, title, year, copies):
        self.title = title
        self.year = year
        self.copies = copies

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if type(value) is not int or value < 1450 or value > 2026:
            raise InvalidYearError(self.title, value)
        self._year = value #this for calling the setter, also to reject a bad year before storing it

    @property
    def copies(self):
        return self._copies

    @copies.setter
    def copies(self, value):
        if type(value) is not int or value < 0:
            raise InvalidCopiesError(self.title, value, "Copies must be a non-negative integer")
        self._copies = value #this for calling the setter, also to rejects -1 and string, it only accepts 6 and 0 and it will store in _copies

    def checkout(self, n):
        if type(n) is not int or n <= 0:
            raise InvalidCopiesError(
                self.title, n, "Checkout amount must be a positive integer")
                
        if n > self.copies:
            raise InvalidCopiesError(
                self.title, n,
                f"Cannot checkout {n} copies of '{self.title}'. "
                f"Only {self.copies} available")
                
            
        self.copies = self.copies - n

    def __str__(self):
        return f"{self.title} ({self.year}): {self.copies} copies available"

    def __repr__(self):
        return f"Book(title='{self.title}', year={self.year}, copies={self.copies})"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False #final return is TRUE only if all 3 comparisons are also true

        return(
            self.title == other.title
            and self.year == other.year
            and self.copies == other.copies
            #the first check avoids trying to read .title from something thats not a book
        )


    @classmethod
    def from_dict(cls,d):
        return cls(d["title"], d["year"], d["copies"])

def build_catalog(raw_rows):
    books = []
    failures = []

    for row in raw_rows:
        try:
            book = Book.from_dict(row)
            books.append(book)
        except CatalogError as e:
            failures.append({"row": row, "error": str(e)})
    return books, failures

def rank_by_availability(books):
    return sorted(books, key=lambda book: book.copies, reverse=True)
     
raw_rows = [
    {"title": "The Pragmatic Coder", "year": 2015, "copies": 6},
    {"title": "Data Structures 101", "year": 2010, "copies": 3},
    {"title": "Ghost Protocols", "year": 3050, "copies": 4},
    {"title": "Legacy Systems", "year": 2001, "copies": -1},
    {"title": "Untitled Draft", "year": 1300, "copies": 2},
    {"title": "Clean Interfaces", "year": 2019, "copies": 0},
    {"title": "Algorithms Illustrated", "year": 2022, "copies": 9},
]

if __name__ == "__main__":
    books, failures = build_catalog(raw_rows)

    print()
    print("-----VALID BOOKS-----")

    for book in books:
        print(book)

    print()
    print("-----INVALID ROWS-----")

    for failure in failures:
        print(f"Skipped row: {failure['row']} -> reason: {failure['error']}")

    print()
    print("-----CHECKOUT ERROR DEMO-----")
    
    trylang_book = Book("Checkout Test", 2016, 2)

    try:
        trylang_book.checkout(3)
    except InvalidCopiesError as e:
        print(e)

    print()
    print("-----BOOKS RANKED BY AVAILABILITY-----")

    ranked_books= rank_by_availability(books)
    for position, book in enumerate(ranked_books, start=1):
        print(f"{position}. {book.title} — {book.copies} copies")
