from faker import Faker
from faker.providers import person, phone_number, internet, isbn, address
from project_1.database.entities import Address, Author, Book, Publisher, Order, User, Review


class BaseMixin(object):
    """Base Mixin"""

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
    """Book Mixin"""
    def __init__(self, fake: Faker):
        super(PersonMixin, self).__init__(fake)
        self._fake.add_provider(person)

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

    def __str__(self):
        return "PersonMixin"


class ISBNMixin(BaseMixin):
    """ISBN Mixin"""
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


class FakeGenerator(AddressMixin, PersonMixin, ISBNMixin):
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
#
#
# class InternetFactory(BaseFactory):
#     """Class used for generating fake Internet data"""
#
#     def __init__(self, fake):
#         """
#         :type fake: Faker
#         """
#         super(InternetFactory, self).__init__(fake, internet)
#
#     def generate_email(self):
#         return self.fake.unique.ascii_free_email()
#
#     def __str__(self):
#         return f"InternetFactory(fake_id={id(self.fake)})"
#
#
# class PhoneNumberFactory(BaseFactory):
#     """Class used for generating fake PhoneNumber data"""
#
#     def __init__(self, fake):
#         """
#         :type fake: Faker
#         """
#         super(PhoneNumberFactory, self).__init__(fake, phone_number)
#
#     def __str__(self):
#         return f"PhoneNumberFactory(fake_id={id(self.fake)})"
#
#
# class ISBNFactory(BaseFactory):
#     """Class used for generating fake ISBN data"""
#
#     def __init__(self, fake):
#         """
#         :type fake: Faker
#         """
#         super(ISBNFactory, self).__init__(fake, isbn)
#
#
#     def __str__(self):
#         return f"ISBNrFactory(fake_id={id(self.fake)})"
