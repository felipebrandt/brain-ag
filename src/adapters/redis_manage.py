import redis
from os import getenv

redis_uri = getenv('URI_REDIS', '')
redis_client = redis.from_url(redis_uri)


def get_key(key):
    return redis_client.get(key).decode('utf-8')


class EnvironmentKeys:
    BASE = 'local'
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
    # redis_client.set('BA_DB', '')
    # redis_client.set('BA_HOST', '')
    # redis_client.set('BA_USER', '')
    # redis_client.set('BA_PASSWORD', '')
    # redis_client.set('BA_PORT', '5432')
    # redis_client.set('BA_DBL', 'brain_agriculture')
    # redis_client.set('BA_HOSTL', 'localhost')
    # redis_client.set('BA_USERL', 'postgres')
    # redis_client.set('BA_PASSWORDL', 'Pohgma@1980')
    # redis_client.set('BA_PORTL', '5432')
    pass








