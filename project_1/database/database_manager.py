import functools

import psycopg2
from psycopg2.extras import execute_values


def safe_connection(error_msg=None):
    """
    A decorator that wraps the passed in function closes the db connection
    """
    def _check_authorization(method):
        @functools.wraps(method)
        def wrapper(db_manager, *args, **kwargs):
            try:
                return method(db_manager, *args, **kwargs)
            except(Exception, psycopg2.Error) as error:
                print(error_msg)
                db_manager.close()
                raise error
        return wrapper
    return _check_authorization


class ComicBooksDBManager(object):
    """DB Wrapper for the comic books database"""

    def __init__(self):
        self._conn = None
        self._cursor = None

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
                INSERT INTO "2016_author" (gender, name, nationality)
                VALUES %s
                """
        values = [author.to_list() for author in data.values()]
        execute_values(cur=self._cursor, sql=sql, argslist=values)

    @safe_connection("Error executing commit method")
    def commit(self):
        """Commit the changes to the database"""
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
