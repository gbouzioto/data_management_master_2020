import json
import os

from project_1.database.entities import Author, Book, Publisher, BookAuthor, Review


class UCSDJsonDataParser(object):
    """ Parser for handling the json data"""
    DEFAULT_DATA_PATH = os.path.join(os.path.dirname(".."), "raw_data")
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
        self._valid_data = {"authors": {}, "books": {}}

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
        key of the book. Publisher entities are also created here.
        """
        file_path = os.path.join(self.data_path, self.books_filename)
        with open(file_path) as fin:
            for line in fin:
                book_data = json.loads(line)
                book_id = book_data.get("book_id")
                book_isbn = book_data.get("isbn")
                if book_id and book_isbn and len(book_isbn) == 10:

                    # initialize a book dictionary, it will contain a Book and it can contain a Publisher,
                    # BookAuthor and Review objects and starts with a 0 author ordinal
                    book_relations = {"book_authors": {}, "author_ordinal": 0, "reviews": []}

                    # create a Book
                    book = Book()
                    book.isbn = book_isbn
                    title = book_data.get("title")
                    book.title = title if len(title) <= 200 else None
                    publication_year = book_data.get("publication_year")
                    book.publication_year = publication_year if len(publication_year) == 4 else None
                    description = book_data.get("description")
                    book.description = description if description else None

                    # create a publisher if data is sufficient
                    if publisher_name := book_data.get("publisher"):
                        publisher = Publisher()
                        publisher.name = publisher_name
                        book_relations["publisher"] = publisher

                    # add author relations if they can be added
                    if authors := book_data.get("authors"):
                        for author in authors:
                            author_id = author.get("author_id")
                            if author_id in self._valid_data["authors"].keys():
                                validated_author = self._valid_data["authors"][author_id]
                                book_author = BookAuthor()
                                book_author.author = validated_author
                                book_relations["author_ordinal"] += 1
                                role = author.get("role")
                                book_author.role = role if role else None
                                book_author.ordinal = book_relations["author_ordinal"]
                                book_relations["book_authors"][author_id] = book_author

                    book_relations["book"] = book
                    self._valid_data["books"][book_id] = book_relations

    def _process_reviews(self):
        """
        Processes the review data and keeps only the reviews that are valid. A valid review must at least
        have a text field, reference a book id that is already parsed and have a valid rating.
        """
        file_path = os.path.join(self.data_path, self.reviews_filename)
        with open(file_path) as fin:
            for line in fin:
                review_data = json.loads(line)
                book_id = review_data.get("book_id")
                text = review_data.get("review_text")
                rating = review_data.get("rating")
                if text and self._validate_review_rating(rating) and book_id in self._valid_data["books"].keys():
                    review = Review()
                    created = review_data.get("date_added")
                    review.text = text
                    review.score = rating
                    review.created = created if created else None
                    self._valid_data["books"][book_id]["reviews"].append(review)

    @staticmethod
    def _validate_review_rating(review_rating: int):
        """
        Validates that a review rating is valid (it takes values from 1 - 5)
        :param review_rating: the review rating
        :rtype: bool
        """
        return review_rating in range(1, 6)

    def get_parsed_author_data(self):
        """
        :returns: The author data parsed
        """
        return self._valid_data["authors"]

    def get_parsed_book_data(self):
        """
        :returns: The book data parsed
        """
        return self._valid_data["books"]
