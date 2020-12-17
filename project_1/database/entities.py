"""Database entities"""


class BaseEntity(object):
    """BaseEntity Object"""
    @classmethod
    def build_from_data(cls, data: dict):
        """Builds the object from the given data"""
        obj = cls()
        for key, value in data.items():
            if hasattr(obj, key):
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

    def to_list(self):
        return [self.gender, self.name, self.nationality]


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

    def to_dict(self):
        return {"address_name": self.address_name, "address_number": self.address_number,
                "city": self.city, "country": self.country, "postal_code": self.postal_code}


class Book(BaseEntity):
    """Represents a Book entity"""

    def __init__(self):
        self.isbn = None
        self.title = None
        self.publication_year = None
        self.current_price = None
        self.description = None
        self.publisher = None

    def __str__(self):
        return f"Book(book_id={self.isbn})"

    def to_dict(self):
        return {"isbn": self.isbn, "title": self.title, "publication_year": self.publication_year,
                "current_price": self.current_price, "description": self.description}


class Publisher(BaseEntity):
    """Represents a Publisher entity"""

    def __init__(self):
        self.address = None
        self.name = None
        self.phone_number = None

    def __str__(self):
        return f"Publisher(name={self.name})"

    def to_dict(self):
        return {"name": self.name, "address": self.address, "phone_number": self.phone_number}


class Order(BaseEntity):
    """Represents a Order entity"""

    def __init__(self):
        self.user = None
        self.billing_address = None
        self.shipping_address = None
        self.placement = None
        self.completed = None

    def __str__(self):
        return f"Order(user={self.user})"


class User(BaseEntity):
    """Represents a User entity"""

    def __init__(self):
        self.username = None
        self.password = None
        self.phone_number = None
        self.email = None
        self.real_name = None

    def __str__(self):
        return f"User(username={self.username})"

    def to_dict(self):
        return {"username": self.username, "password": self.password, "phone_number": self.phone_number,
                "email": self.email, "real_name": self.real_name}


class Review(BaseEntity):
    """Represents a Review entity"""

    def __init__(self):
        self.nickname = None
        self.created = None
        self.score = None
        self.text = None

    def __str__(self):
        return f"Review(nickname={self.nickname})"

    def to_dict(self):
        return {"nickname": self.nickname, "created": self.created, "score": self.score,
                "text": self.text}


class BookReview(BaseEntity):
    """Represents a BookReview entity"""

    def __init__(self):
        self.book = None
        self.review = None

    def __str__(self):
        return f"BookReview(book={self.book}, review=({self.review})"


class BookAuthor(BaseEntity):
    """Represents a BookAuthor entity"""

    def __init__(self):
        self.author = None
        self.book = None
        self.ordinal = None
        self.role = None

    def __str__(self):
        return f"BookAuthor(book={self.book}, author=({self.author})"


class BookOrder(BaseEntity):
    """Represents a BookOrder entity"""

    def __init__(self):
        self.book = None
        self.order = None
        self.quantity = None

    def __str__(self):
        return f"BookOrder(book={self.book}, order=({self.order})"


class UserAddress(BaseEntity):
    """Represents a UserAddress entity"""

    def __init__(self):
        self.address = None
        self.user = None
        self.is_physical = None
        self.is_shipping = None
        self.is_billing = None
        self.is_active = None

    def __str__(self):
        return f"UserAddress(address={self.address}, user=({self.user})"
