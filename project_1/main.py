import os
import sys
import argparse

from project_1.database.database_manager import DBManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from project_1.parser.parser import UCSDJsonDataParser


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--database', help="the name of the database", required=True)
    arg_parser.add_argument('-pwd', '--password', help="password for the specified database user", required=True)
    arg_parser.add_argument('-u', '--user', nargs='?', default="postgres", help="database user, defaults to postgres")
    arg_parser.add_argument('-i', '--ip', nargs='?', default="localhost", help="connection ip, defaults to localhost")
    arg_parser.add_argument('-p', '--port', nargs='?', default="5432", help="connection port, defaults to 5432")
    args = arg_parser.parse_args()

    # json_parser = UCSDJsonDataParser()
    # json_parser.process_data()

    db_manager = DBManager.create(database=args.database, password=args.password, user=args.user,
                                  host=args.ip, port=args.port)


if "__main__" == __name__:
    main()
