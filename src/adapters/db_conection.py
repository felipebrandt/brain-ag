from peewee import *
from src.adapters.redis_manage import EnvironmentKeys


ENVIRON = EnvironmentKeys()
if ENVIRON.BASE == 'local':
    db = PostgresqlDatabase(database=ENVIRON.DBL,
                       host=ENVIRON.HOSTL,
                       port=ENVIRON.PORTL,
                       user=ENVIRON.USERL,
                       password=ENVIRON.PASSWORDL)
else:
    db = PostgresqlDatabase(database=ENVIRON.DB,
                       host=ENVIRON.HOST,
                       port=ENVIRON.PORT,
                       user=ENVIRON.USER,
                       password=ENVIRON.PASSWORD)