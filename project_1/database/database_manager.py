import functools

import psycopg2
from psycopg2.extras import execute_values


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
        self._present_authors = None

    def __str__(self):
        return f"ComicBooksDBManager(db_id={id(self._conn)})"

    def close(self):
        self._cursor.close()
        self._conn.close()

    @safe_connection("Error executing insert authors method")
    def insert_authors(self, data):
        """
        Inserts all the authors provided in the data
        :param data: {"author_id": database.entities.Author}
        """
        sql = """
                insert into "2016_author" (gender, name, nationality)
                values %s
                """
        values = [author.to_list() for author in data.values()]
        execute_values(cur=self._cursor, sql=sql, argslist=values)
        self._conn.commit()
        self._present_authors = len(values)

    @safe_connection("Error executing insert relations method")
    def insert_relations(self, book_data):
        """
        Inserts all data from the book_data gathered along with their relations.
        :param book_data: {book_id: {"book": "database.entities.Book",
                           "book_authors": [database.entities.BookAuthor],
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
        author_sql = """
            insert into "2016_author"(gender, name, nationality)
            values (%s, %s, %s)
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
        cur_author_id = self._present_authors
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
                for book_author in book_authors:
                    self._cursor.execute(author_sql, [book_author.author.gender, book_author.author.name,
                                                      book_author.author.nationality])
                    cur_author_id += 1
                    self._cursor.execute(book_author_sql, [cur_author_id, cur_book_id, book_author.ordinal,
                                                           book_author.role])
            # Review and Book Review query
            if reviews := data.get("reviews"):
                for review in reviews:
                    self._cursor.execute(review_sql, [review.created, review.score, review.text])
                    cur_review_id += 1
                    self._cursor.execute(book_review_sql, [cur_book_id, cur_review_id])
            cur_book_id += 1
            self._conn.commit()

    @safe_connection("Error executing commit method")
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
