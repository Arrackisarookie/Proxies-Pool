import requests
import re
from requests.exceptions import ConnectionError

base_headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/74.0.3729.131 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    headers = dict(base_headers, **options)
    print('Crawling', url)
    proxy = get_proxy()
    proxies = {"http": proxy}
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        print('Got the page', url)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('Failed to Crawl', url)
        return None


def isIP(str):
    pattern = re.compile(r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)')
    return re.match(pattern, str)


def get_proxy():
    url = 'http://localhost:5000/random'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
