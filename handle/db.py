import redis
from handle.utils import isIP
from random import choice
from handle.setting import REDIS_HOST, REDIS_PORT, REDIS_KEY, REDIS_PASSWORD
from handle.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from handle.error import PoolEmptyError


class RedisClient(object):
    def __init__(
        self, host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD
    ):
        self.db = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            decode_responses=True
        )

    def add(self, proxy, score=INITIAL_SCORE):
        if not isIP(proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            self.db.zincrby(REDIS_KEY, -1, proxy)
            return score - 1
        else:
            print('Current Score:', score, 'Remove')
            self.db.zrem(REDIS_KEY, proxy)

    def remove(self, proxy):
        print('Proxy:', proxy, 'removed')
        return self.db.zrem(REDIS_KEY, proxy)

    def exist(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})
        return MAX_SCORE

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)
