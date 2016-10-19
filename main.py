from src.crawler.web_crawler import Crawler
from src.pickler import UserPickler
from src.neo4j_persistence.entry import PersistentLayer

class PersistentBiz:
    def __init__(self, user_picker):
        self.up = user_picker


    def crawl_user_reviews(self, uid):
        try:
            reviews = self.up.load_reviews(uid)
        except:
            reviews = Crawler.get_user_reivews(uid)
            self.up.save_review(reviews, uid)
        return reviews


    def crawl_user_rels(self, uid):
        try:
            rels = self.up.load_rels(uid)
        except:
            rels = Crawler.get_followed(uid)
            self.up.save_rels(rels, uid)
        return rels


    def persist_user_reviews(self, user):
        uid = user["id"]
        reviews = self.crawl_user_reviews(uid)
        print("length(reviews): {}".format(len(reviews)))
        if len(reviews) != 0:
            PersistentLayer.insert_reviews(user, reviews)
            return True, reviews
        else:
            return False, reviews


    def persist_user_rels(self, user):
        uid = user["id"]
        rels = self.crawl_user_rels(uid)
        print(rels)
        print("length(rels): {}".format(len(rels)))
        if len(rels) != 0:
            PersistentLayer.insert_followed(user, rels)
            return True, rels
        else:
            return False, rels


def main():
    target_user = {"id": "194275696", "name": "target_xx"}
    peristent_biz = PersistentBiz(UserPickler(target_user))
    peristent_biz.persist_user_reviews(target_user)

    rels_result = peristent_biz.persist_user_rels(target_user)
    rels = rels_result[1]

    count = 0
    max_loop = 99
    for rel in rels:
        user = {"name": rel[0], "id": rel[1]}
        if not peristent_biz.persist_user_reviews(user)[0]:
            print("persist user info failed: user: {}, id: {} ".format(user["name"], user["id"]))
        count += 1
        print("rel loop: {}".format(count))
        if count == max_loop: break




if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))