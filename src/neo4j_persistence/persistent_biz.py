from .entry import PersistentLayer
from ..crawler.web_crawler import Crawler


class PersistentBiz:
    @staticmethod
    def create_rels(user):
        """

        :param user:
         - name: string
         - id: string
        :return:
        """

        followed = Crawler.get_followed(user["id"])
        PersistentLayer.insert_followed(user, followed)


