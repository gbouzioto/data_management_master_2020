import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from project_1.flow.flow import run_exercise


if "__main__" == __name__:
    run_exercise()
