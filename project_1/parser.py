import json
import os

class JsonDataParser(object):
    """ Parser for handling the json data"""
    DEFAULT_DATA_PATH = os.path.join(os.getcwd(), "raw_data")

    def __init__(self, data_path=None):
        """
        :param data_path: path to the files containing the json data, defaults to DEFAULT_DATA_PATH
        """
        self.data_path = data_path if data_path else self.DEFAULT_DATA_PATH
        self.parsed_data = {}

    def load_data(self, file_names: list, key_names: list):
        """
        Loads data for multiple files
        :param file_names: A list of file names
        :param key_names:  A list of key names
        """
        file_size = len(file_names)
        key_size = len(set(key_names))
        if not file_size == key_size:
            raise ValueError(f"Insufficient number of keys: {key_size}"
                             f" provided compared, to files: {file_size}")
        for i in range(file_size):
            self._load_data_from_file(file_names[i], key_names[i])

    def _load_data_from_file(self, file_name: str, key_name: str):
        """
        Loads data from a file.
        :param file_name: file name of the file to be parsed
        :param key_name: key name under which the file contents will be stored
        """
        file_path = os.path.join(self.data_path, file_name)
        with open(file_path) as fin:
            data = (json.loads(line) for line in fin)
        self.parsed_data[key_name] = data


def main():
    json_parser = JsonDataParser()
    files = ["goodreads_book_authors.json", "goodreads_books_comics_graphic.json", "goodreads_reviews_comics_graphic.json"]
    keys = ["authors", "books", "reviews"]
    json_parser.load_data(files, keys)
    pass


if "__main__" == __name__:
    main()
