import redis
from os import getenv

redis_uri = getenv('URI_REDIS', '')
redis_client = redis.from_url(redis_uri)


def get_key(key):
    return redis_client.get(key).decode('utf-8')


class EnvironmentKeys:
    BASE = getenv('BASE', 'local')
    DB = get_key('BA_DB')
    HOST = get_key('BA_HOST')
    USER = get_key('BA_USER')
    PASSWORD = get_key('BA_PASSWORD')
    PORT = int(get_key('BA_PORT'))
    DBL = get_key('BA_DBL')
    HOSTL = get_key('BA_HOSTL')
    USERL = get_key('BA_USERL')
    PASSWORDL = get_key('BA_PASSWORDL')
    PORTL = int(get_key('BA_PORTL'))


if __name__ == '__main__':
    pass









