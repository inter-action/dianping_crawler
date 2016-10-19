import pickle
import os
from pathlib import Path

PROJECT_ROOT_PATH = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')).resolve()
DATA_PATH = PROJECT_ROOT_PATH.joinpath("data")
if not DATA_PATH.exists():
    DATA_PATH.mkdir()

DEFAULT_REVIEW_FILENAME = "latest_reviews.pickle"

class Pickler:
    @staticmethod
    def save_review(reviews, filename=DEFAULT_REVIEW_FILENAME):
        filepath = DATA_PATH.joinpath(filename)
        # An arbitrary collection of objects supported by pickle.
        with filepath.open("wb") as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(reviews, f, pickle.HIGHEST_PROTOCOL)


    @staticmethod
    def load_reviews(filename=DEFAULT_REVIEW_FILENAME):
        return Pickler.load(filename)


    @staticmethod
    def load(filename):
        filepath = DATA_PATH.joinpath(filename)
        if not (filepath.exists() and filepath.is_file()):
            raise RuntimeError("target file <{}> not existed".format(filepath))
        with filepath.open("rb") as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            data = pickle.load(f)
            return data
