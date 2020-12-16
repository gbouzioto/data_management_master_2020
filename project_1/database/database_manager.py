import psycopg2


class DBManager(object):
    """DB Wrapper"""

    def __init__(self):
        self._db = None
        self._cursor = None

    def __str__(self):
        return f"DBManager(db_id={id(self._db)})"

    @classmethod
    def create(cls, database, password, user="postgres", host="localhost", port="5432"):
        """
        :param database: the name of the database
        :param password: password for the specified database user
        :param user: database user - defaults to postgres
        :param host: host ip - defaults to localhost
        :param port: connection port - defaults to 5432
        :rtype: DatabaseManager
        """
        db_manager = cls()
        try:
            db = psycopg2.connect(database=database, password=password, user=user, host=host, port=port)
            cursor = db.cursor()
            db_manager._db = db
            db_manager._cursor = cursor
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print(f"You are connected into the - {record}\n")
            print(f"DSN details: {db.get_dsn_parameters()}\n")
            return db_manager
        except(Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL database", error)
