# -*- coding:utf-8 -*-
"""
@desc: 
"""

MYSQL_PARAMETERS = {
    "host": "localhost",
    "port": 3306,
    "user": "user",
    "password": "password",
    "database": "database",
    "charset": "utf8",
    "maxconnections": 10,
    "maxusage": 1000
}

ELASTICSEARCH_HOSTS = ['localhost:9200']

MONGODB_PARAMETERS = {
    "host": "localhost",
    "port": 27017,
    "username": "username",
    "password": "password",
    "authSource": "admin"
}
MONGODB_URI = None

# REDIS
REDIS_CLS = "redis.StrictRedis"
REDIS_ENCODING = 'utf-8'
# Sane connection defaults.
REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': REDIS_ENCODING,
}