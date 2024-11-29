import redis
from os import getenv

redis_uri = getenv('URI_REDIS', '')
redis_client = redis.from_url(redis_uri)


def get_key(key):
    return redis_client.get(key).decode('utf-8')


class EnvironmentKeys:
    BASE = getenv('BASE', '')
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
    print('')
    # redis_client.set('DB', 'defaultdb')
    # redis_client.set('HOST', '')
    # redis_client.set('USER', '')
    # redis_client.set('PASSWORD', '')
    # redis_client.set('PORT', '5432')
    # redis_client.set('DBL', '')
    # redis_client.set('HOSTL', '')
    # redis_client.set('USERL', '')
    # redis_client.set('PASSWORDL', '')
    # redis_client.set('PORTL', '5432')
    pass









