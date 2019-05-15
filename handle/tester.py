from handle.db import RedisClient
from handle.setting import VALID_STATUS_CODE, BATCH_TEST_SIZE, TEST_URL, MAX_SCORE
from aiohttp.client_exceptions import ClientProxyConnectionError, ClientOSError, ClientResponseError, ServerDisconnectedError
from handle.ignore import ignore_aiohttp_ssl_eror
import aiohttp
import asyncio
import time
import sys


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            ignore_aiohttp_ssl_eror(asyncio.get_running_loop())
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            try:
                real_proxy = 'http://' + proxy
                async with session.get(TEST_URL, proxy=real_proxy, timeout=10, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODE:
                        print('Available:', proxy, 'Current score:', self.redis.max(proxy))
                    else:
                        self.redis.decrease(proxy)
                        print('Status_Code:', response.status, 'IP:', proxy)
            except (
                AttributeError,
                asyncio.TimeoutError,
                ConnectionRefusedError,
                ClientProxyConnectionError,
                ClientOSError,
                ClientResponseError,
                ServerDisconnectedError
            ):
                print('Failed to request', proxy, 'Current score:', self.redis.decrease(proxy))

    def run(self):
        print('Tester started...')
        try:
            count = self.redis.count()
            print('Totally', count, 'proxies now.')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('\nTesting the No.', start+1, '-', stop, 'proxy\n')
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()

                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))

                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('Something Wrong appeared in Tester:', e.args)
