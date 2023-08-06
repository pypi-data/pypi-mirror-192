# -*- coding:utf-8 -*-
"""
@desc: 
"""
import logging
from urllib.parse import quote_plus

import pika
from pika.exceptions import AMQPError

logger = logging.getLogger('pika')

from . import defaults

PARAMETERS_MAP = {
    'RABBITMQ_URL': 'url',
    'RABBITMQ_HOST': 'host',
    'RABBITMQ_PORT': 'port',
    'RABBITMQ_USERNAME': 'username',
    'RABBITMQ_PASSWORD': 'password',
    'RABBITMQ_HEARTBEAT': 'heartbeat',
    'RABBITMQ_CREDENTIALS': 'credentials',
    'RABBITMQ_VIRTUAL_HOST': 'virtual_host',
}


def get_rabbit_from_settings(settings):
    """Returns a rabbit client instance from given Scrapy settings object.
    """
    parameters = defaults.RABBITMQ_PARAMETERS.copy()
    parameters.update(settings.getdict('RABBITMQ_PARAMETERS'))
    for source, dest in PARAMETERS_MAP.items():
        val = settings.get(source)
        if val:
            parameters[dest] = val

    # 处理用户名和密码，首先从username和password取，未取到再用credentials
    if all([parameters.get('username'), parameters.get('password')]):
        parameters['credentials'] = (parameters['username'], parameters['password'])
    parameters.pop('username', None)
    parameters.pop('password', None)
    if parameters.get('credentials'):
        parameters['credentials'] = pika.PlainCredentials(*parameters.get('credentials'))
    else:
        parameters.pop('credentials', None)
    connection = pika.BlockingConnection(pika.ConnectionParameters(**parameters))
    management_port = settings.get('RABBITMQ_MANAGEMENT_PORT') or defaults.RABBITMQ_MANAGEMENT_PORT
    management_scheme = settings.get('RABBITMQ_MANAGEMENT_SCHEME') or defaults.RABBITMQ_MANAGEMENT_SCHEME
    connection.mangement_url = get_management_url(management_scheme, management_port, parameters)
    connection.settings = settings
    connection.reconnect = lambda: reconnect(settings=settings)
    return connection


# Backwards compatible alias.
from_settings = get_rabbit_from_settings


def reconnect(settings):
    times = 0
    while times <= 3:
        try:
            connection = from_settings(settings=settings)
            return connection
        except:
            times += 1
            logger.warning('connect failed {} times'.format(times))

    else:
        raise AMQPError('reconnect failed')


def get_management_url(scheme, port, parameters):
    credentials = ':'.join(map(lambda value: quote_plus(value), parameters['credentials']))
    return '{scheme}://{credentials}@{host}:{port}'.format(
        scheme=scheme,
        credentials=credentials,
        host=parameters['host'],
        port=port,
    )
