raw_rows = [
    {"title": "The Pragmatic Coder", "year": 2015, "copies": 6},
    {"title": "Data Structures 101", "year": 2010, "copies": 3},
    {"title": "Ghost Protocols", "year": 3050, "copies": 4},
    {"title": "Legacy Systems", "year": 2001, "copies": -1},
    {"title": "Untitled Draft", "year": 1300, "copies": 2},
    {"title": "Clean Interfaces", "year": 2019, "copies": 0},
    {"title": "Algorithms Illustrated", "year": 2022, "copies": 9},
]

class CatalogError (Exception):
    def __init__(self, message, title, value):
        super().__init__(message)
        self.title = title
        self.value = value

class InvalidYearError (CatalogError):
    def __init__(self, message, title, value):
        super().__init__(message, title, value)

class InvalidCopiesError (CatalogError):
    def __init__(self, message, title, value):
        super().__init__(message, title, value)

class Book:

    def __init__(self, title, year, copies):
        self.title = title
        self.year = year
        self.copies = copies

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        if year < 1450 or year > 2026:
            raise InvalidYearError(f"{self.title} has invalid year {year}", self.title, year)
        self._year = year
        
    @property
    def copies(self):
        return self._copies

    @copies.setter
    def copies(self, copies):
        if not isinstance(copies, int) or copies < 0:
            raise InvalidCopiesError(f"{self.title} has invalid copies {copies}", self.title, copies)
        self._copies = copies

    def checkout(self, n):
        if n > self._copies:
            raise InvalidCopiesError(f"{self.title} needs {n - self._copies} more copies", self.title, n)
        self._copies -= n

    def __str__(self):
        return f"{self.title} ({self.year}): {self.copies} copies available"

    def __repr__(self):
        return f"Book(title='{self.title}', year={self.year}, copies={self.copies})"

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.title == other.title and self.year == other.year and self.copies == other.copies
        return False

    @classmethod
    def from_dict(cls, d):
        return cls(d['title'], d['year'], d['copies'])

def build_catalog(raw_rows):
    books = []
    failures = []
        
    for row in raw_rows:
        try:
            book = Book.from_dict(row)
            books.append(book)
        except CatalogError as e:
            failures.append({
                "row": row,
                "error": str(e)
            })
    return books, failures

def rank_by_availability(books):
    return sorted(books, key=lambda book: book.copies, reverse=True)

if __name__ == "__main__":
    hobbit = Book("The Hobbit", 1937, 5)
    books, failures = build_catalog(raw_rows)
    ranked_books = rank_by_availability(books)

    for book in books:
        print(book)

    for failure in failures:
        print(f"Skipped row: {failure['row']} -> reason: {failure['error']}")

    hobbit.checkout(1)
    try:
        hobbit.checkout(5)
    except InvalidCopiesError as e:
        print(f"Error: {e}")

    for number, book in enumerate(ranked_books, start=1):
        print(f"{number}. {book.title} — {book.copies} copies")