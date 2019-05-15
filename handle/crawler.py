from handle.utils import get_page
from pyquery import PyQuery as pq
import time


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v, in attrs.items():
            if 'crawl' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('Succeed to get a proxy:', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_kaidaili(self, page_count=100):
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(2, page_count + 1)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#list table tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    if ip and port:
                        yield ':'.join([ip, port])
            time.sleep(5)
