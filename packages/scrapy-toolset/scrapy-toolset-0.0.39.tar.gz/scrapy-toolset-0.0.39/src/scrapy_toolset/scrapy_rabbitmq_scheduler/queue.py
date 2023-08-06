# -*- coding:utf-8 -*-
"""
@desc: 
"""
import traceback
import uuid
import logging
from copy import deepcopy
from urllib.parse import quote_plus, urljoin

import pika
import requests
from pika.exceptions import ChannelClosedByBroker, AMQPError
from scrapy.utils.reqser import request_to_dict, request_from_dict

from . import picklecompat, defaults
from .connection import reconnect, get_rabbit_from_settings

logger = logging.getLogger(__name__)
pika_logger = logging.getLogger('pika').setLevel(logging.ERROR)

from scrapy import Request

class Queue(object):
    arguments = None

    def __init__(self, spider, key, serializer=None):
        """

        :param server:
        :param spider:
        :param key:
        :param serializer:
        """
        if serializer is None:
            serializer = picklecompat
        if not hasattr(serializer, 'loads'):
            raise TypeError("serializer does not implement 'loads' function: %r"
                            % serializer)
        if not hasattr(serializer, 'dumps'):
            raise TypeError("serializer '%s' does not implement 'dumps' function: %r"
                            % serializer)
        self.server = get_rabbit_from_settings(settings=spider.settings)
        self.spider = spider
        # 进行消息push时指定的routing_key, requests和start_urls不同
        self.routing_key = key
        self.request_queue_name = spider.scheduler_routing_keys['request']
        self.error_request_queue_name = spider.scheduler_routing_keys['error']
        self.serializer = serializer
        self.declared_queues = set()
        self.channel_pool = {}
        # get some settings from spider
        self.durable = spider.settings.getbool('SCHEDULER_PERSIST', True)
        self.auto_ack = spider.settings.getbool('SCHEDULER_AUTOACK', False)
        self.virtual_host = spider.settings.get('RABBITMQ_VIRTUAL_HOST') or spider.settings.getdict(
            'RABBITMQ_PARAMETERS').get('virtual_host') or '/'
        self.exchange = spider.settings.get('RABBITMQ_EXCHANGE') or defaults.RABBITMQ_EXCHANGE
        self.start_url_encoding = spider.settings.get('START_URL_ENCODING') or defaults.START_URL_ENCODING

    def queue_init(self, queues):
        """
        声明爬虫运行过程所需要的所有队列和交换机
        一般来说是这三个队列
        start_urls requests errors
        :return:
        """
        channel = self.server.channel()
        channel.exchange_declare(self.exchange, arguments={"x-dead-letter-exchange": ""}, durable=self.durable)
        # 声明start_urls队列
        channel.queue_declare(queue=queues['start_urls'], durable=self.durable)
        # 声明请求队列
        channel.queue_declare(queues['requests'], kwargs={
            "x-dead-letter-routing-key": queues['errors'],
            "x-dead-letter-exchange": self.exchange
        }, durable=self.durable)
        # 声明错误队列
        channel.queue_declare(queues['errors'], durable=self.durable)
        # 队列绑定
        for routing_key in queues.values():
            channel.queue_bind(routing_key, self.exchange)
        channel.close()

    def shovel(self):
        # merge错误队列,只针对请求队列
        try:
            data = {
                "value": {
                    "src-uri": "amqp://",
                    "src-queue": self.error_request_queue_name,
                    "src-delete-after": "queue-length",
                    "dest-uri": "amqp://",
                    "dest-queue": self.request_queue_name
                }
            }
            requests.put(
                urljoin(self.http_api,
                        f'/api/parameters/shovel/{quote_plus(self.virtual_host)}/{self.error_request_queue_name}'),
                json=data)
        except Exception as e:
            logger.error('错误队列合并失败:{}'.format(traceback.format_exc()))

    def _encode_request(self, request):
        """Encode a request object"""
        return self.encode_request(request)

    def encode_request(self, request):
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    def __len__(self):
        """Return the length of the queue"""
        try:
            response = requests.get(
                urljoin(self.server.api, f'/api/queues/{quote_plus(self.virtual_host)}/{self.routing_key}')).json()

            return response.get("messages", 0)
        except:
            logger.error('get message count failed.')
            logger.error(traceback.format_exc())
            return 0

    def push(self, request, raw=False, routing_key=None):
        """Push a request"""
        raise NotImplementedError

    def pop(self, raw=False):
        """Pop a request"""
        # 偶尔断开连接一般发生在这里
        try:
            channel = self.server.channel()
        except AMQPError:
            # 重连
            logger.warning('AMQPError, retrying....')
            self.server = reconnect(self.server.settings)
            channel = self.server.channel()
        method, properrties, body = channel.basic_get(queue=self.routing_key, auto_ack=self.auto_ack)
        if body is not None:
            if raw:
                return self.serializer.loads(body.decode(self.start_url_encoding)), channel
            else:
                rabbitmq_channel_id = uuid.uuid4().__str__()
                self.channel_pool[rabbitmq_channel_id] = channel
                logger.debug('获取一条消息...')
                request = self._decode_request(encoded_request=body)
                request.meta['rabbitmq_channel_id'] = rabbitmq_channel_id
                return request
        else:
            channel.close()

    def fetch(self, batch_size, raw=False):
        """Pop many message"""
        for i in range(batch_size):
            yield self.pop(raw=raw)

    def clear(self):
        """Clear queue/stack"""
        for key in [self.request_queue_name, self.error_request_queue_name,
                    getattr(self.spider, 'start_urls_routing_key', None)]:
            if key:
                with self.server.channel() as channel:
                    try:
                        channel.queue_delete(key)
                    except ChannelClosedByBroker as e:
                        if e.args[0] == 404:
                            pass
                        else:
                            logger.error('删除队列失败.')
                    except Exception as e:
                        logger.error('删除队列失败.')

    def ack(self, request: Request, is_start_url=False):
        if is_start_url:
            rabbitmq_channel_id = request.meta.get("start_rabbitmq_channel_id")
        else:
            rabbitmq_channel_id = request.meta.get("rabbitmq_channel_id")
        channel = self.channel_pool.pop(rabbitmq_channel_id, None)
        if channel:
            if not channel.is_closed:
                channel.basic_ack(1)
                channel.close()
                logger.debug('ack success.')
            else:
                logger.debug('ack failed, channel have cloesd.')
        else:
            logger.debug('ack failed, channel does not exists.')

    def nack(self, request: Request, requeue=False, replace_request=None):
        """发生错误时处理"""
        rabbitmq_channel_id = request.meta.get("rabbitmq_channel_id")
        channel = self.channel_pool.pop(rabbitmq_channel_id, None)
        if channel:
            if not channel.is_closed:
                if requeue:
                    # 一般发生在重试时，直接进入原队列即可
                    channel.basic_nack(1, requeue=requeue)
                else:
                    # 将该请求放入错误队列, 如果存在father_request， 则将father_request放入错误队列
                    father_request = request.meta.get('father_request')
                    if father_request:
                        # 需要删除father_request的ack方法和nack方法，否则无法pickle
                        self.push(father_request, raw=False, routing_key=self.error_request_queue_name)
                        # 已经将该请求的父级放入错误队列，那么当前请求可以ack
                        channel.basic_ack(1)
                    else:
                        # 如果替换请求不为空，则将替换请求扔进错误队列，为了处理重试达到上限时该请求归队时仍是重试上限请求
                        if replace_request is not None:
                            self.push(replace_request, raw=False, routing_key=self.error_request_queue_name)
                            channel.basic_ack(1)
                        else:
                            channel.basic_nack(1, requeue=requeue)
                channel.close()
                logger.debug('nack success.')
            else:
                logger.debug('nack faild, channel have cloesd.')
        else:
            logger.debug('nack faild, channel does not exists.')




class Base(object):
    arguments = None

    def __init__(self, spider, key, serializer=None):
        """

        :param server:
        :param spider:
        :param key:
        :param serializer:
        """
        if serializer is None:
            serializer = picklecompat
        if not hasattr(serializer, 'loads'):
            raise TypeError("serializer does not implement 'loads' function: %r"
                            % serializer)
        if not hasattr(serializer, 'dumps'):
            raise TypeError("serializer '%s' does not implement 'dumps' function: %r"
                            % serializer)
        self.server = get_rabbit_from_settings(settings=spider.settings)
        self.spider = spider
        # 进行消息push时指定的routing_key, requests和start_urls不同
        self.routing_key = key
        self.request_queue_name = spider.scheduler_routing_keys['request']
        self.error_request_queue_name = spider.scheduler_routing_keys['error']
        self.serializer = serializer
        self.declared_queues = set()
        self.channel_pool = {}
        # get some settings from spider
        self.durable = spider.settings.getbool('SCHEDULER_PERSIST', True)
        self.auto_ack = spider.settings.getbool('SCHEDULER_AUTOACK', False)
        self.virtual_host = spider.settings.get('RABBITMQ_VIRTUAL_HOST') or spider.settings.getdict(
            'RABBITMQ_PARAMETERS').get('virtual_host') or '/'
        self.exchange = spider.settings.get('RABBITMQ_EXCHANGE') or defaults.RABBITMQ_EXCHANGE
        self.start_url_encoding = spider.settings.get('START_URL_ENCODING') or defaults.START_URL_ENCODING

    def queue_init(self, queues):
        """
        声明爬虫运行过程所需要的所有队列和交换机
        一般来说是这三个队列
        start_urls requests errors
        :return:
        """
        channel = self.server.channel()
        channel.exchange_declare(self.exchange, arguments={"x-dead-letter-exchange": ""}, durable=self.durable)
        # 声明start_urls队列
        channel.queue_declare(queue=queues['start_urls'], durable=self.durable)
        # 声明请求队列
        channel.queue_declare(queues['requests'], kwargs={
            "x-dead-letter-routing-key": queues['errors'],
            "x-dead-letter-exchange": self.exchange
        }, durable=self.durable)
        # 声明错误队列
        channel.queue_declare(queues['errors'], durable=self.durable)
        # 队列绑定
        for routing_key in queues.values():
            channel.queue_bind(routing_key, self.exchange)
        channel.close()

    def shovel(self):
        # merge错误队列,只针对请求队列
        try:
            data = {
                "value": {
                    "src-uri": "amqp://",
                    "src-queue": self.error_request_queue_name,
                    "src-delete-after": "queue-length",
                    "dest-uri": "amqp://",
                    "dest-queue": self.request_queue_name
                }
            }
            requests.put(
                urljoin(self.http_api,
                        f'/api/parameters/shovel/{quote_plus(self.virtual_host)}/{self.error_request_queue_name}'),
                json=data)
        except Exception as e:
            logger.error('错误队列合并失败:{}'.format(traceback.format_exc()))

    def _encode_request(self, request):
        """Encode a request object"""
        return self.encode_request(request)

    def encode_request(self, request):
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    def __len__(self):
        """Return the length of the queue"""
        try:
            response = requests.get(
                urljoin(self.server.api, f'/api/queues/{quote_plus(self.virtual_host)}/{self.routing_key}')).json()

            return response.get("messages", 0)
        except:
            logger.error('get message count failed.')
            logger.error(traceback.format_exc())
            return 0

    def push(self, request, raw=False, routing_key=None):
        """Push a request"""
        raise NotImplementedError

    def pop(self, raw=False):
        """Pop a request"""
        # 偶尔断开连接一般发生在这里
        try:
            channel = self.server.channel()
        except AMQPError:
            # 重连
            logger.warning('AMQPError, retrying....')
            self.server = reconnect(self.server.settings)
            channel = self.server.channel()
        method, properrties, body = channel.basic_get(queue=self.routing_key, auto_ack=self.auto_ack)
        if body is not None:
            if raw:
                return self.serializer.loads(body.decode(self.start_url_encoding)), channel
            else:
                rabbitmq_channel_id = uuid.uuid4().__str__()
                self.channel_pool[rabbitmq_channel_id] = channel
                logger.debug('获取一条消息...')
                request = self._decode_request(encoded_request=body)
                request.meta['rabbitmq_channel_id'] = rabbitmq_channel_id
                return request
        else:
            channel.close()

    def fetch(self, batch_size, raw=False):
        """Pop many message"""
        for i in range(batch_size):
            yield self.pop(raw=raw)

    def clear(self):
        """Clear queue/stack"""
        for key in [self.request_queue_name, self.error_request_queue_name,
                    getattr(self.spider, 'start_urls_routing_key', None)]:
            if key:
                with self.server.channel() as channel:
                    try:
                        channel.queue_delete(key)
                    except ChannelClosedByBroker as e:
                        if e.args[0] == 404:
                            pass
                        else:
                            logger.error('删除队列失败.')
                    except Exception as e:
                        logger.error('删除队列失败.')

    def ack(self, request: Request, is_start_url=False):
        if is_start_url:
            rabbitmq_channel_id = request.meta.get("start_rabbitmq_channel_id")
        else:
            rabbitmq_channel_id = request.meta.get("rabbitmq_channel_id")
        channel = self.channel_pool.pop(rabbitmq_channel_id, None)
        if channel:
            if not channel.is_closed:
                channel.basic_ack(1)
                channel.close()
                logger.debug('ack success.')
            else:
                logger.debug('ack failed, channel have cloesd.')
        else:
            logger.debug('ack failed, channel does not exists.')

    def nack(self, request: Request, requeue=False, replace_request=None):
        """发生错误时处理"""
        rabbitmq_channel_id = request.meta.get("rabbitmq_channel_id")
        channel = self.channel_pool.pop(rabbitmq_channel_id, None)
        if channel:
            if not channel.is_closed:
                if requeue:
                    # 一般发生在重试时，直接进入原队列即可
                    channel.basic_nack(1, requeue=requeue)
                else:
                    # 将该请求放入错误队列, 如果存在father_request， 则将father_request放入错误队列
                    father_request = request.meta.get('father_request')
                    if father_request:
                        # 需要删除father_request的ack方法和nack方法，否则无法pickle
                        self.push(father_request, raw=False, routing_key=self.error_request_queue_name)
                        # 已经将该请求的父级放入错误队列，那么当前请求可以ack
                        channel.basic_ack(1)
                    else:
                        # 如果替换请求不为空，则将替换请求扔进错误队列，为了处理重试达到上限时该请求归队时仍是重试上限请求
                        if replace_request is not None:
                            self.push(replace_request, raw=False, routing_key=self.error_request_queue_name)
                            channel.basic_ack(1)
                        else:
                            channel.basic_nack(1, requeue=requeue)
                channel.close()
                logger.debug('nack success.')
            else:
                logger.debug('nack faild, channel have cloesd.')
        else:
            logger.debug('nack faild, channel does not exists.')


class FifoQueue(Base):
    """Per-spider FIFO queue"""

    def push(self, request, raw=False, routing_key=None, encoding="utf-8"):
        """push a request"""
        _routing_key = routing_key or self.routing_key
        channel = self.server.channel()
        channel.confirm_delivery()
        channel.basic_publish(self.exchange, routing_key=_routing_key,
                              body=self.serializer.dumps(request).encode(encoding) if raw else self._encode_request(
                                  request),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # 消息持久化
                              ))
        channel.close()


class PriorityQueue(Base):
    arguments = {"x-max-priority": 255}

    def push(self, request, raw=False, routing_key=None, encoding="utf-8"):
        """push a request"""
        _routing_key = routing_key or self.routing_key
        channel = self.server.channel()
        if raw:
            priority = 1
        else:
            priority = request.meta.get("priority") or 1
        channel.confirm_delivery()
        channel.basic_publish(self.exchange, routing_key=_routing_key,
                              body=self.serializer.dumps(request).encode(encoding) if raw else self._encode_request(
                                  request),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                                  priority=priority
                              ))
        channel.close()
