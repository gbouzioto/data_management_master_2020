import os
import sys

from project_1.parser.parser import UCSDJsonDataParser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def main():
    json_parser = UCSDJsonDataParser()
    json_parser.process_data()


if "__main__" == __name__:
    main()
