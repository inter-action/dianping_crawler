from crawler import web_crawler


def main():
    web_crawler.kick_start()

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))