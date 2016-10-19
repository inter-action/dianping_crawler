from .crawler.web_crawler import Crawler
from .pickler import Pickler

def main():
    try:
        reviews = Pickler.load_reviews()
    except RuntimeError:
        reviews = Crawler.get_user_reivews("194275696")
        Pickler.save_review(reviews)
    print(reviews)
    print("length: {}".format(len(reviews)))

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))