import json
import os

from project_1.database.entities import Author, Book, Publisher, BookAuthor


class UCSDJsonDataParser(object):
    """ Parser for handling the json data"""
    DEFAULT_DATA_PATH = os.path.join(os.getcwd(), "raw_data")
    AUTHORS_FILENAME = "goodreads_book_authors.json"
    BOOKS_FILENAME = "goodreads_books_comics_graphic.json"
    REVIEWS_FILENAME = "goodreads_reviews_comics_graphic.json"

    def __init__(self, data_path=None, authors_filename=None, books_filename=None, reviews_filename=None):
        """
        :param data_path: path to the files containing the json data, defaults to DEFAULT_DATA_PATH
        :param authors_filename: filename that contains the author data
        :param books_filename: filename that contains the book data
        :param reviews_filename: filename that contains the review data
        """
        self.data_path = data_path if data_path else self.DEFAULT_DATA_PATH
        self.authors_filename = authors_filename if authors_filename else self.AUTHORS_FILENAME
        self.books_filename = books_filename if books_filename else self.BOOKS_FILENAME
        self.reviews_filename = reviews_filename if reviews_filename else self.REVIEWS_FILENAME
        self._valid_data = {"authors": {}, "books": {}, "reviews": {}}

    def process_data(self):
        """
        Processes the data provided, in the following order: authors, books, reviews.
        If any of the data is not loaded returns immediately.
        """
        self._process_authors()
        self._process_books()
        self._process_reviews()

    def _process_authors(self):
        """
        Processes the author data and keeps only the authors that are valid.
        A valid author must at least have an id and a name.
        """
        file_path = os.path.join(self.data_path, self.authors_filename)
        with open(file_path) as fin:
            for line in fin:
                author_data = json.loads(line)
                author_name = author_data.get("name")
                author_id = author_data.get("author_id")
                if author_name and author_id:
                    author = Author()
                    author.name = author_name
                    self._valid_data["authors"][author_id] = author

    def _process_books(self):
        """
        Processes the book data and keeps only the books that are valid.
        A valid book must at least have an isbn and an id. Moreover creates the book_authors relations.
        These are created by searching the authors dictionary given the author ids contained in the 'authors'
        key of the book. In order to avoid duplicate entries afterwards, the author ids found will be removed
        from the initial authors found.
        """
        file_path = os.path.join(self.data_path, self.books_filename)
        author_ids = set()
        with open(file_path) as fin:
            for line in fin:
                book_data = json.loads(line)
                book_id = book_data.get("book_id")
                book_isbn = book_data.get("isbn")
                if book_id and book_isbn:

                    # initialize a book dictionary, it will contain a Book and it can contain a Publisher,
                    # BookAuthor and Review objects
                    book_relations = {"book_authors": [], "author_ordinal": 0}

                    # create a Book
                    book = Book()
                    book.isbn = book_isbn
                    title = book_data.get("title")
                    book.title = title if title else None
                    publication_year = book_data.get("publication_year")
                    book.publication_year = publication_year if publication_year else None
                    description = book_data.get("description")
                    book.description = description if description else None

                    # create a publisher if data is sufficient
                    publisher_name = book_data.get("publisher")
                    if publisher_name:
                        publisher = Publisher()
                        publisher.name = publisher_name
                        book_relations["publisher"] = publisher

                    # add author relations
                    if authors := book_data.get("authors"):
                        for author in authors:
                            author_id = author.get("author_id")
                            validated_author = self._valid_data["authors"].get(author_id)
                            if validated_author:
                                book_author = BookAuthor()
                                book_author.author = validated_author
                                book_relations["author_ordinal"] += 1
                                role = author.get("role")
                                book_author.role = role if role else None
                                book_author.ordinal = book_relations["author_ordinal"]
                                author_ids.add(author_id)
                                book_relations["book_authors"].append(book_author)

                    book_relations["book"] = book
                    self._valid_data["books"][book_id] = book_relations

    def _process_reviews(self):
        """
        Processes the author data and keeps only the authors that are valid. A valid author must at least
        have an id and a name.
        """
        pass


def main():
    json_parser = UCSDJsonDataParser()
    json_parser.process_data()


if "__main__" == __name__:
    main()
