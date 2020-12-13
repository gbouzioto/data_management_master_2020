"""Database entities"""


class Author(object):
    """Represents an Author entity"""
    def __init__(self):
        self.author_id = None
        self.name = None
        self.nationality = None
        self.gender = None

    def __str__(self):
        return f"Author(author_id={self.author_id})"


class Address(object):
    """Represents an Address entity"""
    def __init__(self):
        self.address_name = None
        self.address_number = None
        self.city = None
        self.country = None
        self.postal_code = None

    def __str__(self):
        return f"Address(address={self.address_name + self.address_number + self.city})"


class Book(object):
    """Represents a Book entity"""

    def __init__(self):
        self.book_id = None
        self.isbn = None
        self.isbn13 = None
        self.title = None
        self.publication_year = None
        self.current_price = None
        self.description = None
        self.publisher = None
        self.authors = []
        self.reviews = []

    def __str__(self):
        return f"Book(book_id={self.book_id})"


class Publisher(object):
    """Represents a Publisher entity"""

    def __init__(self):
        self.address = None
        self.name = None
        self.phone_number = None

    def __str__(self):
        return f"Publisher(address={self.address.__str__()})"
