import pickle
from . import constants

PROJECT_ROOT_PATH = constants.PROJECT_ROOT_PATH
DATA_PATH = constants.DATA_PATH
if not DATA_PATH.exists():
    DATA_PATH.mkdir()


class Pickler:
    @staticmethod
    def save_data(data, filename):
        filepath = DATA_PATH.joinpath(filename)
        # An arbitrary collection of objects supported by pickle.
        with filepath.open("wb") as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


    @staticmethod
    def load_data(filename):
        filepath = DATA_PATH.joinpath(filename)
        if not (filepath.exists() and filepath.is_file()):
            raise RuntimeError("target file <{}> not existed".format(filepath))
        with filepath.open("rb") as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            data = pickle.load(f)
            return data


class UserPickler:
    user_reviews_tpl = "latest_reviews-{}.pickle"
    user_rels_tpl = "rels-{}.pickle"

    def __init__(self, user):
        self.user = user
        self.uid = str(user["id"])
        userpath = DATA_PATH.joinpath(self.uid)
        if not userpath.exists():
            userpath.mkdir()


    def load_reviews(self, id):
        return Pickler.load_data(self.get_review_filename(id))


    def save_review(self, reviews, id):
        return Pickler.save_data(reviews, self.get_review_filename(id))


    def get_review_filename(self, id):
        return self._get_user_path(self.user_reviews_tpl.format(id))

    def _get_user_path(self, part):
        return "{}/{}".format(self.uid, part)

    def get_rels_filename(self, id):
        return self._get_user_path(self.user_rels_tpl.format(id))


    def load_rels(self, id):
        return Pickler.load_data(self.get_rels_filename(id))


    def save_rels(self, data, id):
        return Pickler.save_data(data, self.get_rels_filename(id))
