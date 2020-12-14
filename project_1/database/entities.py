"""Database entities"""
from faker import Faker
from faker.providers import person, phone_number, internet, isbn, address


class Author(object):
    """Represents an Author entity"""
    def __init__(self):
        self.name = None
        self.nationality = None
        self.gender = None

    def __str__(self):
        return f"Author(author_id={self.name + self.nationality})"


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
        return f"Book(book_id={self.isbn})"


class Publisher(object):
    """Represents a Publisher entity"""

    def __init__(self):
        self.address = None
        self.name = None
        self.phone_number = None

    def __str__(self):
        return f"Publisher(address={self.address.__str__()})"


class User(object):
    """Represents a User entity"""

    def __init__(self):
        self.username = None
        self.password = None
        self.phone_number = None
        self.email = None
        self.real_name = None
        self.addresses = []

    def __str__(self):
        return f"User(email={self.email})"


class BaseFactory(object):
    """Base Class used for generating fake data"""

    def __init__(self, fake, *providers):
        """
        :type fake: Faker
        :type providers: faker.providers.Provider
        """
        self.fake = fake
        if providers:
            for provider in providers:
                self.fake.add_provider(provider)

    def __str__(self):
        return f"BaseFactory(fake_id={id(self.fake)})"


class AddressFactory(BaseFactory):
    """Class used for generating fake Address data"""

    def __init__(self, fake):
        """
        :type fake: Faker
        """
        super(AddressFactory, self).__init__(fake, address)

    def __str__(self):
        return f"AddressFactory(fake_id={id(self.fake)})"


class PersonFactory(BaseFactory):
    """Class used for generating fake Person data"""

    def __init__(self, fake):
        """
        :type fake: Faker
        """
        super(PersonFactory, self).__init__(fake, person)

    def generate_name_and_gender(self):
        gender = 'Male' if self.fake.random.randint(0, 1) == 0 else 'Female'
        name = " ".join((self.fake.first_name_male(), self.fake.last_name_male())) \
            if gender == 'Male' else " ".join((self.fake.first_name_female(), self.fake.last_name_female()))
        return gender, name

    def generate_name(self):
        return " ".join((self.fake.first_name(), self.fake.last_name()))

    def generate_gender(self):
        return 'Male' if self.fake.random.randint(0, 1) == 0 else 'Female'

    def __str__(self):
        return f"PersonFactory(fake_id={id(self.fake)})"


class InternetFactory(BaseFactory):
    """Class used for generating fake Internet data"""

    def __init__(self, fake):
        """
        :type fake: Faker
        """
        super(InternetFactory, self).__init__(fake, internet)

    def generate_email(self):
        return self.fake.unique.ascii_free_email()

    def __str__(self):
        return f"InternetFactory(fake_id={id(self.fake)})"


class PhoneNumberFactory(BaseFactory):
    """Class used for generating fake PhoneNumber data"""

    def __init__(self, fake):
        """
        :type fake: Faker
        """
        super(PhoneNumberFactory, self).__init__(fake, phone_number)

    def __str__(self):
        return f"PhoneNumberFactory(fake_id={id(self.fake)})"


class ISBNFactory(BaseFactory):
    """Class used for generating fake ISBN data"""

    def __init__(self, fake):
        """
        :type fake: Faker
        """
        super(ISBNFactory, self).__init__(fake, isbn)

    def generate_isbn(self):
        return self.fake.unique.isbn10()

    def generate_isbn_13(self):
        return self.fake.unique.isbn13()

    def __str__(self):
        return f"ISBNrFactory(fake_id={id(self.fake)})"
