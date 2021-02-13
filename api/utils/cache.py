from api.config import Config
import redis
import typing

redis = redis.from_url(Config.REDIS_URL)

## expiry in seconds
def set_value(key, value, expiry=300):
    redis.set(key, value, expiry)

def get_value(key):
    return redis.get(key)