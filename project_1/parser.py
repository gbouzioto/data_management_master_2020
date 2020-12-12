import json
import os


class JsonDataParser(object):
    """ Parser for handling the json data"""
    DEFAULT_DATA_PATH = os.path.join("project_1", "raw_data")

    def __init__(self, data_path=None):
        """
        :param data_path: the path to the files containing the json data
        """
        self.data_path = data_path if data_path else self.DEFAULT_DATA_PATH
        self.parsed_data = {}

    def load_data(self, file_name, key_name):
        """
        :param file_name: file name of the file to be parsed
        :param key_name: key name under which the file contents will be stored
        """
        data = []
        file_path = os.path.join(self.data_path, file_name)
        with open(file_path) as fin:
            for line in fin:
                d = json.loads(line)
                data.append(d)
        self.parsed_data[key_name] = data
