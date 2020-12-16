import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from project_1.database.database_manager import ComicBooksDBManager
from project_1.parser.parser import UCSDJsonDataParser, parse_user_args


def main():
    args = parse_user_args()
    json_parser = UCSDJsonDataParser()
    json_parser.process_data()
    author_data = json_parser.get_parsed_author_data()
    book_data = json_parser.get_parsed_book_data()

    db_manager = ComicBooksDBManager.create(database=args.database, password=args.password, user=args.user,
                                            host=args.ip, port=args.port)
    db_manager.truncate_tables()
    db_manager.insert_authors(author_data)
    db_manager.insert_relations(book_data)
    db_manager.close()


if "__main__" == __name__:
    main()
