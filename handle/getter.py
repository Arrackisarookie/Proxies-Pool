from handle.db import RedisClient
from handle.crawler import Crawler
from handle.setting import POOL_UPPER_THRESSHOLD


class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER_THRESSHOLD:
            return True
        return False

    def run(self):
        print('Getter starts...')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    if not self.redis.exist(proxy):
                        self.redis.add(proxy)
