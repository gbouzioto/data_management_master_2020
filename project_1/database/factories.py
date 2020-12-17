import decimal
import random
from faker import Faker
from faker.providers import person, phone_number, internet, isbn, address, date_time, lorem, misc
from project_1.database.entities import Address, Author, Book, Publisher, User, Review, UserAddress, BookOrder, Order


class BaseMixin(object):
    """BaseMixin"""

    def __init__(self, fake: Faker):
        self._fake = fake

    def __str__(self):
        return "BaseMixin"


class AddressMixin(BaseMixin):
    """Address Mixin"""
    def __init__(self, fake: Faker):
        super(AddressMixin, self).__init__(fake)
        self._fake.add_provider(address)

    def address_name(self):
        return self._fake.street_name()

    def address_number(self):
        return self._fake.building_number()

    def country(self):
        return self._fake.country()

    def city(self):
        return self._fake.city()

    def postal_code(self):
        return self._fake.postcode()

    def __str__(self):
        return "AddressMixin"


class PersonMixin(BaseMixin):
    """BookMixin"""
    def __init__(self, fake: Faker):
        super(PersonMixin, self).__init__(fake)
        self._fake.add_provider(person)
        self._fake.add_provider(phone_number)

    def name_and_gender(self):
        gender = 'Male' if self._fake.random.randint(0, 1) == 0 else 'Female'
        name = " ".join((self._fake.first_name_male(), self._fake.last_name_male())) \
            if gender == 'Male' else " ".join((self._fake.first_name_female(), self._fake.last_name_female()))
        return gender, name

    def name(self):
        return " ".join((self._fake.first_name(), self._fake.last_name()))

    def gender(self):
        return 'Male' if self._fake.random.randint(0, 1) == 0 else 'Female'

    def nationality(self):
        # Nationality is not included in Faker, so return language instead
        return self._fake.language_name()

    def phone_number(self):
        return self._fake.phone_number()

    def __str__(self):
        return "PersonMixin"


class ISBNMixin(BaseMixin):
    """ISBNMixin"""
    def __init__(self, fake: Faker):
        super(ISBNMixin, self).__init__(fake)
        self._fake.add_provider(isbn)

    def isbns(self, n=1):
        """
        :param n: Number of unique isbns to be generated
        """
        return (self._fake.unique.isbn10() for _ in range(n))

    def __str__(self):
        return "ISBNMixin"


class DateTimeMixin(BaseMixin):
    """DateTimeMixin"""
    def __init__(self, fake: Faker):
        super(DateTimeMixin, self).__init__(fake)
        self._fake.add_provider(date_time)

    def year(self):
        return self._fake.year()

    def timestamp(self):
        return self._fake.date_time()

    def __str__(self):
        return "DateTimeMixin"


class LoremMixin(BaseMixin):
    """LoremMixin"""
    def __init__(self, fake: Faker):
        super(LoremMixin, self).__init__(fake)
        self._fake.add_provider(lorem)

    def sentence(self, nb_words=10):
        """
        :param nb_words: Number of words to be included
        """
        return self._fake.sentence(nb_words=nb_words)

    def text(self):
        return self._fake.text()

    def __str__(self):
        return "LoremMixin"


class MiscMixin(BaseMixin):
    """MiscMixin"""
    def __init__(self, fake: Faker):
        super(MiscMixin, self).__init__(fake)
        self._fake.add_provider(misc)
        self._fake.add_provider(internet)

    def emails(self, n=1):
        """
        :param n: Number of unique emails to be generated
        """
        return (self._fake.unique.email() for _ in range(n))

    def usernames(self, n=1):
        """
        :param n: Number of unique usernames to be generated
        """
        return (self._fake.unique.user_name() for _ in range(n))

    def password(self, length=10):
        """
        :param length: password length
        """
        return self._fake.password(length=length)

    def nickname(self):
        return self._fake.user_name()

    @staticmethod
    def score():
        return random.randint(1, 5)

    @staticmethod
    def money():
        return decimal.Decimal(random.randrange(10000))/100

    def __str__(self):
        return "MiscMixin"


class FakeGenerator(AddressMixin, PersonMixin, ISBNMixin, DateTimeMixin, LoremMixin, MiscMixin):
    """Class used for generating fake data"""

    def __init__(self):
        self._fake = Faker()
        super(FakeGenerator, self).__init__(self._fake)

    def clear_unique(self):
        """Clears the unique data generated"""
        self._fake.unique.clear()

    def __str__(self):
        return f"_FakeGenerator(fake_id={id(self._fake)})"


_fg = FakeGenerator()


class AddressFactory(object):
    """Class used for generating fake Address entities"""

    @staticmethod
    def generate_addresses(n=1):
        """
        Generator of Address objects
        :param n: number of objects to be generated
        """
        for i in range(n):
            data = {"address_name": _fg.address_name(), "address_number": _fg.address_number(),
                    "city": _fg.city(), "country": _fg.country(), "postal_code": _fg.postal_code()}
            yield Address.build_from_data(data)

    def __str__(self):
        return "AddressFactory"


class AuthorFactory(object):
    """Class used for generating fake Author data"""

    @staticmethod
    def generate_authors(n=1):
        """
        Generator of Author objects
        :param n: number of objects to be generated
        """
        for i in range(n):
            name, gender = _fg.name_and_gender()
            data = {"name": name, "gender": gender, "nationality": _fg.nationality()}
            yield Author.build_from_data(data)

    def __str__(self):
        return "AuthorFactory"


class PublisherFactory(object):
    """Class used for generating fake Publisher data"""

    @staticmethod
    def generate_publishers(n=1):
        """
        Generator of Publisher objects
        :param n: number of objects to be generated
        """
        for i in range(n):
            data = {"name": _fg.name(), "phone_number": _fg.phone_number()}
            yield Publisher.build_from_data(data)

    @staticmethod
    def add_address(publisher: Publisher, publisher_address=None):
        if not publisher_address:
            publisher.address = AddressFactory.generate_addresses()
        else:
            publisher.address = publisher_address

    def __str__(self):
        return "PublisherFactory"


class BookFactory(object):
    """Class used for generating fake Book data"""

    @staticmethod
    def generate_books(n=1):
        """
        Generator of Book objects
        :param n: number of objects to be generated
        """
        isbns = list(_fg.isbns(n=n))
        for i in range(n):
            data = {"isbn": isbns[i], "publication_year": _fg.year(), "title": _fg.sentence(),
                    "description": _fg.text(), "current_price": _fg.money()}
            yield Book.build_from_data(data)
        _fg.clear_unique()

    @staticmethod
    def add_publisher(book: Book, publisher=None):
        if not publisher:
            book.publisher = PublisherFactory.generate_publishers()
        else:
            book.publisher = publisher

    def __str__(self):
        return "BookFactory"


class UserFactory(object):
    """Class used for generating fake User data"""

    @staticmethod
    def generate_users(n=1):
        """
        Generator of User objects
        :param n: number of objects to be generated
        """
        emails = list(_fg.emails(n=n))
        usernames = list(_fg.usernames(n=n))
        for i in range(n):
            data = {"username": usernames[i], "email": emails[i], "password": _fg.password(),
                    "real_name": _fg.name(), "phone_number": _fg.phone_number()}
            yield User.build_from_data(data)
        _fg.clear_unique()

    def __str__(self):
        return "UserFactory"


class ReviewFactory(object):
    """Class used for generating fake Review data"""

    @staticmethod
    def generate_reviews(n=1):
        """
        Generator of Review objects
        :param n: number of objects to be generated
        """
        for i in range(n):
            data = {"nickname": _fg.nickname(), "text": _fg.text(), "score": _fg.score(),
                    "created": _fg.timestamp()}
            yield Review.build_from_data(data)

    def __str__(self):
        return "ReviewFactory"


class UserAddressFactory(object):
    """Class used for generating fake UserAddress data"""

    @staticmethod
    def generate_user_addresses(user_address_mapper, user_num=1, addresses_per_user=1):
        """
        Generator of UserAddress objects
        :param user_address_mapper: dict that holds the mapping of user_id -> address_id
        :param user_num: number of users
        :param addresses_per_user: number of addresses per user
        """
        for i in range(1, user_num + 1):
            user_address_mapper[i] = []
            for j in range(i, i + addresses_per_user):
                data = {"address": j, "user": i, "is_physical": True,
                        "is_shipping": True, "is_billing": True, "is_active": True}
                user_address_mapper[i].append(j)
                yield UserAddress.build_from_data(data)

    def __str__(self):
        return "UserAddressFactory"


class OrderFactory(object):
    """Class used for generating fake UserAddress data"""

    @staticmethod
    def generate_orders(user_address_mapper, user_num=1, order_per_user=1):
        """
        Generator of UserAddress objects
        :param user_address_mapper: dict that holds the mapping of user_id -> address_id
        :param user_num: number of users
        :param order_per_user: number of orders per user
        """
        for i in range(1, user_num + 1):
            for j in range(i, i + order_per_user):
                data = {"user": i, "billing_address": user_address_mapper[i][0],
                        "shipping_address": user_address_mapper[i][0], "placement": _fg.timestamp()}
                yield Order.build_from_data(data)

    def __str__(self):
        return "OrderFactory"


class BookOrderFactory(object):
    """Class used for generating fake UserAddress data"""

    @staticmethod
    def generate_book_orders(book_num=10, order_num=10):
        """
        Generator of UserAddress objects
        :param book_num: number of books available
        :param order_num: number of total orders
        """
        for i in range(1, order_num + 1):
            data = {"book": random.randint(1, book_num), "order": i, "quantity": random.randint(1, 4)}
            yield BookOrder.build_from_data(data)

    def __str__(self):
        return "BookOrderFactory"
