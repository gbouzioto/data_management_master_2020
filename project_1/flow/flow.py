import argparse

from project_1.database.database_manager import ComicBooksDBManager
from project_1.parser.parser import UCSDJsonDataParser

FLOW_HELP_TEXT = """
flow of the program, defaults to main. It has 3 options:
    -main: parses the dataset and inserts the actual data into the db
    -test: provided that main flow has been executed at least once or the database contains its data 
    creates a handful of user, orders and addresses for testing
    -test_rb: clears the tables that were used by the test in order for the database to contain clean data.
    """


def _parse_user_args():
    """
    Parses the user arguments
    :returns: user arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--database', help="the name of the database", required=True)
    arg_parser.add_argument('-pwd', '--password', help="password for the specified database user", required=True)
    arg_parser.add_argument('-u', '--user', nargs='?', default="postgres", help="database user, defaults to postgres")
    arg_parser.add_argument('-i', '--ip', nargs='?', default="localhost", help="connection ip, defaults to localhost")
    arg_parser.add_argument('-p', '--port', nargs='?', default="5432", help="connection port, defaults to 5432")
    arg_parser.add_argument('-f', '--flow', help=FLOW_HELP_TEXT, default="main", choices=["main", "test", "test_rb"])
    return arg_parser.parse_args()


def _main_flow(args):
    """
    Described in FLOW_HELP_TEXT
    :param args: user arguments
    """
    # Parse data
    json_parser = UCSDJsonDataParser()
    json_parser.process_data()
    author_data = json_parser.get_parsed_author_data()
    book_data = json_parser.get_parsed_book_data()

    # Establish the db connection and create the data
    db_manager = ComicBooksDBManager.create(database=args.database, password=args.password, user=args.user,
                                            host=args.ip, port=args.port)
    db_manager.truncate_tables()
    db_manager.insert_authors(author_data)
    db_manager.insert_relations(book_data)
    db_manager.close()


def _test_flow(args):
    """
    Described in FLOW_HELP_TEXT
    :param args: user arguments
    """
    db_manager = ComicBooksDBManager.create(database=args.database, password=args.password, user=args.user,
                                            host=args.ip, port=args.port)
    db_manager.create_test_data()
    db_manager.close()


def _test_rb_flow(args):
    """
    Described in FLOW_HELP_TEXT
    :param args: user arguments
    """
    db_manager = ComicBooksDBManager.create(database=args.database, password=args.password, user=args.user,
                                            host=args.ip, port=args.port)
    db_manager.clear_test_data()
    db_manager.close()


def run_exercise():
    args = _parse_user_args()
    flows = {"main": _main_flow, "test": _test_flow, "test_rb": _test_rb_flow}
    flows[args.flow](args)