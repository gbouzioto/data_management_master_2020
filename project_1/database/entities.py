"""Database entities"""


class BaseEntity(object):
    """BaseEntity Object"""
    @classmethod
    def build_from_data(cls, data: dict):
        """Builds the object from the given data"""
        obj = cls()
        for key, value in data.items():
            if hasattr(object, key):
                setattr(obj, key, value)
        return obj

    def __str__(self):
        return "BaseEntity"


class Author(BaseEntity):
    """Represents an Author entity"""
    def __init__(self):
        self.name = None
        self.nationality = None
        self.gender = None

    def __str__(self):
        return f"Author(author_id={self.name + self.nationality})"


class Address(BaseEntity):
    """Represents an Address entity"""
    def __init__(self):
        self.address_name = None
        self.address_number = None
        self.city = None
        self.country = None
        self.postal_code = None

    def __str__(self):
        return f"Address(address={self.address_name + self.address_number + self.city})"


class Book(BaseEntity):
    """Represents a Book entity"""

    def __init__(self):
        self.isbn = None
        self.isbn13 = None
        self.title = None
        self.publication_year = None
        self.current_price = None
        self.description = None
        self.publisher = None
        self.authors = None
        self.reviews = None

    def __str__(self):
        return f"Book(book_id={self.isbn})"


class Publisher(BaseEntity):
    """Represents a Publisher entity"""

    def __init__(self):
        self.address = None
        self.name = None
        self.phone_number = None

    def __str__(self):
        return f"Publisher(name={self.name})"


class Order(BaseEntity):
    """Represents a Order entity"""

    def __init__(self):
        self.address = None
        self.book = None
        self.user = None
        self.placement = None
        self.completed = None

    def __str__(self):
        return f"Order(address={self.address}, book= {self.book}, user={self.user})"


class User(BaseEntity):
    """Represents a User entity"""

    def __init__(self):
        self.username = None
        self.password = None
        self.phone_number = None
        self.email = None
        self.real_name = None
        self.addresses = None

    def __str__(self):
        return f"User(username={self.username})"


class Review(BaseEntity):
    """Represents a Review entity"""

    def __init__(self):
        self.nickname = None
        self.created = None
        self.score = None
        self.text = None

    def __str__(self):
        return f"Review(nickname={self.nickname})"
