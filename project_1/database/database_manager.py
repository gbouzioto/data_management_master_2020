import functools
import random

import psycopg2
from psycopg2.extras import execute_values

from project_1.database.factories import (MiscMixin, UserFactory, AddressFactory,
                                          UserAddressFactory, BookOrderFactory, OrderFactory, FakeGenerator)


def safe_connection(error_msg=None):
    """
    A decorator that wraps the passed in function closes the db connection on error safely.
    """
    def _safe_connection(method):
        @functools.wraps(method)
        def wrapper(db_manager, *args, **kwargs):
            try:
                return method(db_manager, *args, **kwargs)
            except(Exception, psycopg2.Error) as error:
                print(error_msg)
                db_manager.close()
                raise error
        return wrapper
    return _safe_connection


class ComicBooksDBManager(object):
    """DB Wrapper for the comic books database"""

    def __init__(self):
        self._conn = None
        self._cursor = None
        self._author_id_mapper = {}

    def __str__(self):
        return f"ComicBooksDBManager(db_id={id(self._conn)})"

    def close(self):
        self._cursor.close()
        self._conn.close()

    def insert_parsed_data(self, author_data, book_data):
        """
        Inserts all parsed data into the database.
        :param author_data: {"author_id": database.entities.Author}
        :param book_data: {book_id: {"book": "database.entities.Book",
                           "book_authors": {author_id: database.entities.BookAuthor},
                           "author_ordinal": int, "reviews": [database.entities.Review],
                           "publisher": database.entities.Publisher}
        """
        self._insert_authors(author_data)
        self._insert_relations(book_data)

    def _insert_authors(self, author_data):
        """
        Inserts all the authors provided in the data
        :param author_data: {"author_id": database.entities.Author}
        """
        sql = """
                insert into "2016_author" (gender, name, nationality)
                values %s
                """
        id_count = 1
        values = []
        for author_id, author_data in author_data.items():
            # map the ids of the authors to the ids in the database
            # so the relation book_author can be filled
            self._author_id_mapper[author_id] = id_count
            values.append(author_data.to_list())
            id_count += 1
        execute_values(cur=self._cursor, sql=sql, argslist=values)
        self._conn.commit()

    def _insert_relations(self, book_data):
        """
        Inserts all data from the book_data gathered along with their relations.
        :param book_data: {book_id: {"book": "database.entities.Book",
                           "book_authors": {author_id: database.entities.BookAuthor},
                           "author_ordinal": int, "reviews": [database.entities.Review],
                           "publisher": database.entities.Publisher}
        """

        pub_sql = """
            insert into "2016_publisher"(name, phone_number, address_id) 
            values (%s, %s, %s)
            """
        book_sql = """
            insert into "2016_book"(isbn, current_price, description, publication_year, title, publisher_id) 
                values (%s, %s, %s, %s, %s, %s)
        """
        review_sql = """
            insert into "2016_review"(created, score, text)
            values (%s, %s, %s)
        """
        book_author_sql = """
            insert into "2016_book_author"(author_id, book_id, author_ordinal, role) 
            values (%s, %s, %s, %s)
        """
        book_review_sql = """
            insert into "2016_book_review"(book_id, review_id) 
            values (%s, %s)
        """
        # initial id values
        cur_book_id = 1
        cur_pub_id = 1
        cur_review_id = 0

        for data in book_data.values():
            book = data["book"]

            # Publisher query
            if publisher := data.get("publisher"):
                self._cursor.execute(pub_sql, [publisher.name, publisher.phone_number, publisher.address])
                book.publisher = cur_pub_id
                cur_pub_id += 1
            # Book query
            self._cursor.execute(book_sql, [book.isbn, book.current_price, book.description,
                                 book.publication_year, book.title, book.publisher])
            # Author and Book Author query
            if book_authors := data.get("book_authors"):
                for author_id, book_author in book_authors.items():
                    self._cursor.execute(book_author_sql, [self._author_id_mapper[author_id],
                                                           cur_book_id, book_author.ordinal,
                                                           book_author.role])
            # Review and Book Review query
            if reviews := data.get("reviews"):
                for review in reviews:
                    self._cursor.execute(review_sql, [review.created, review.score, review.text])
                    cur_review_id += 1
                    self._cursor.execute(book_review_sql, [cur_book_id, cur_review_id])
            cur_book_id += 1
            self._conn.commit()

    @safe_connection("Error in executing commit method")
    def commit(self):
        """Commit the changes to the database"""
        self._conn.commit()

    def truncate_tables(self):
        sql = """select table_name from information_schema.tables where table_schema = 'public'"""
        self._cursor.execute(sql)
        for table_name in self._cursor.fetchall():
            self._truncate_table(table_name)
        self._conn.commit()

    def _truncate_table(self, table_name):
        sql = """truncate "%s" restart identity cascade""" % table_name
        self._cursor.execute(sql)

    @safe_connection("Error in executing create test data method")
    def create_test_data(self, user_num=10, order_per_user=5, address_per_user=3):
        """
        Creates data for testing. Note that this method modifies the book price on actual data.
        If you want to restore their price to its previous value you will have to turn the first
        (user_num x order_per_user) book ids back to null manually. For simplicity it is assumed that
        the user always buys the same book in his order x  book_order_per_user times and that his
        billing address is the same as his shipping address.

        :param user_num: number of Fake users to be created
        :param order_per_user: number of Fake orders per user
        :param address_per_user: number of Fake addresses per user
        """
        book_sql = """update "2016_book" set current_price=%s where book_id=%s"""
        user_sql = """
           insert into "2016_user"(username, password, phone_number, email, real_name)
           values %s
        """
        address_sql = """
           insert into "2016_address"(address_name, address_number, city, country, postal_code)
           values %s
        """
        user_address_sql = """
           insert into "2016_user_address"(address_id, user_id, is_physical, is_shipping, is_billing, is_active) 
           values %s
        """
        book_order_sql = """
           insert into "2016_book_order"(book_id, order_id, quantity) 
           values %s
        """
        order_sql = """
           insert into "2016_order"(user_id, billing_address_id, shipping_address_id, placement) 
           values %s
        """

        self.clear_test_data()
        book_ids_num = user_num * order_per_user
        print(f"\n ****** The first {book_ids_num} books were chosen ******\n")
        # create fake prices
        prices = [MiscMixin.money() for _ in range(book_ids_num)]
        for i in range(book_ids_num):
            self._cursor.execute(book_sql, (prices[i], i + 1))
        # create fake users
        users = list(UserFactory.generate_users(user_num))
        values = [[user.username, user.password, user.phone_number, user.email, user.real_name] for user in users]
        execute_values(self._cursor, user_sql, values)
        # create fake addresses
        address_nums = address_per_user * user_num
        addresses = list(AddressFactory.generate_addresses(address_nums))
        values = [[address.address_name, address.address_number, address.city, address.country, address.postal_code]
                  for address in addresses]
        execute_values(self._cursor, address_sql, values)
        # create fake user addresses
        user_address_mapper = {}
        user_addresses = list(UserAddressFactory.generate_user_addresses(user_address_mapper,
                                                                         user_num, address_per_user))
        values = [[user_address.address, user_address.user, user_address.is_physical, user_address.is_shipping,
                   user_address.is_billing, user_address.is_active] for user_address in user_addresses]
        execute_values(self._cursor, user_address_sql, values)
        # create fake orders
        orders = list(OrderFactory.generate_orders(user_address_mapper, user_num, order_per_user))
        values = [[order.user, order.billing_address, order.shipping_address, order.placement] for order in orders]
        execute_values(self._cursor, order_sql, values)
        # create fake book orders
        book_orders = list(BookOrderFactory.generate_book_orders(book_ids_num, len(orders)))
        values = [[book_order.book, book_order.order, book_order.quantity] for book_order in book_orders]
        execute_values(self._cursor, book_order_sql, values)
        self._conn.commit()

    def clear_test_data(self):
        queries = ["""truncate "2016_user", "2016_order", "2016_book_order", "2016_user_address" restart identity""",
                   """delete from "2016_address" """, """alter sequence "2016_address_address_id_seq" RESTART WITH 1"""]
        for query in queries:
            self._cursor.execute(query)
        self._conn.commit()

    def assign_prices_to_books(self):
        book_sql = """update "2016_book" set current_price=%s where book_id=%s"""
        book_sql_id = """select book_id from "2016_book" order by book_id desc limit 1"""
        self._cursor.execute(book_sql_id)
        max_id = self._cursor.fetchone()[0]
        prices = [MiscMixin.money() for _ in range(max_id)]
        for i in range(max_id):
            self._cursor.execute(book_sql, (prices[i], i + 1))
        self._conn.commit()

    def assign_addresses_to_publishers(self):
        publisher_sql = """update "2016_publisher" set address_id=%s where publisher_id=%s"""
        publisher_sql_id = """select publisher_id from "2016_publisher" order by publisher_id desc limit 1"""
        address_sql_id = """select address_id from "2016_address" order by address_id desc limit 1"""
        self._cursor.execute(publisher_sql_id)
        max_pub_id = self._cursor.fetchone()[0]
        self._cursor.execute(address_sql_id)
        max_address_id = self._cursor.fetchone()[0]
        for i in range(max_pub_id):
            random_id = random.randint(1, max_address_id)
            self._cursor.execute(publisher_sql, (random_id, i + 1))
        self._conn.commit()

    def assign_gender_nationality_to_authors(self):
        author_sql = """update "2016_author" set gender=%s, nationality=%s where author_id=%s"""
        author_sql_id = """select author_id from "2016_author" order by author_id desc limit 1"""
        self._cursor.execute(author_sql_id)
        max_author_id = self._cursor.fetchone()[0]
        gen = FakeGenerator()
        for i in range(max_author_id):
            random_gender = gen.gender()
            random_nationality = gen.nationality()
            self._cursor.execute(author_sql, (random_gender, random_nationality, i + 1))
        self._conn.commit()

    @classmethod
    def create(cls, database, password, user="postgres", host="localhost", port="5432"):
        """
        :param database: database name
        :param password: password for the specified database user
        :param user: database user - defaults to postgres
        :param host: host ip - defaults to localhost
        :param port: connection port - defaults to 5432
        :rtype: ComicBooksDBManager
        """
        db_manager = cls()
        try:
            conn = psycopg2.connect(database=database, password=password, user=user, host=host, port=port)
            cursor = conn.cursor()
            db_manager._conn = conn
            db_manager._cursor = cursor
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print(f"You are connected into the - {record}\n")
            print(f"DSN details: {conn.get_dsn_parameters()}\n")
            return db_manager
        except(Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL database", error)
