# -*- coding:utf-8 -*-
"""
@desc: 
"""
import six
import logging
import importlib

from scrapy.utils.misc import load_object

from . import connection, defaults

logger = logging.getLogger(__name__)


class Scheduler(object):

    def __init__(self, server,
                 flush_on_start=False,
                 merge_error_on_start=False,
                 queue_key=defaults.SCHEDULER_QUEUE_KEY,
                 start_urls_key=defaults.START_URLS_KEY,
                 queue_cls=defaults.SCHEDULER_QUEUE_CLASS,
                 dupefilter_cls='scrapy.dupefilters.RFPDupeFilter',
                 idle_before_close=0,
                 serializer=None,
                 ack_on_item_error=False,
                 ack_on_item_dropped=False
                 ):
        """

        :param server: rabbitmq connection
        :param flush_on_start: Whether to flush requests when closing. Default is False.
        :param queue_key: Requests queue key.
        :param queue_cls: Importable path to the queue class.
        :param idle_before_close:  Timeout before giving up.
        :param serializer: serializer
        """
        if idle_before_close < 0:
            raise TypeError("idle_before_close cannot be negative")

        self.server = server
        self.flush_on_start = flush_on_start
        self.merge_error_on_start = merge_error_on_start
        self.queue_key = queue_key
        self.start_urls_key = start_urls_key
        self.queue_cls = queue_cls
        self.dupefilter_cls = dupefilter_cls
        self.idle_before_close = idle_before_close
        self.serializer = serializer
        self.stats = None
        self.ack_on_item_error = ack_on_item_error
        self.ack_on_item_dropped = ack_on_item_dropped

    @classmethod
    def from_settings(cls, settings):
        kwargs = {
            'flush_on_start': settings.getbool('SCHEDULER_FLUSH_ON_START'),
            'merge_error_on_start': settings.getbool('SCHEDULER_MERGE_ERROR_ON_START'),
            'idle_before_close': settings.getint('SCHEDULER_IDLE_BEFORE_CLOSE'),
        }
        optional = {
            'queue_key': 'SCHEDULER_QUEUE_KEY',
            'start_urls_key': 'START_URLS_KEY',
            'queue_cls': 'SCHEDULER_QUEUE_CLASS',
            'dupefilter_cls': 'DUPEFILTER_CLASS',
            'serializer': 'SCHEDULER_SERIALIZER'
        }
        for name, setting_name in optional.items():
            val = settings.get(setting_name)
            if val:
                kwargs[name] = val

        # Support serializer as a path to a module.
        if isinstance(kwargs.get('serializer'), six.string_types):
            kwargs['serializer'] = importlib.import_module(kwargs['serializer'])

        server = connection.from_settings(settings)
        return cls(server=server, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        instance = cls.from_settings(settings)
        instance.stats = crawler.stats
        return instance

    def open(self, spider):
        self.spider = spider
        try:
            self.queue = load_object(self.queue_cls)(
                server=self.server,
                spider=spider,
                key=self.queue_key % {'spider': spider.name},
                serializer=self.serializer,
            )
        except TypeError as e:
            raise ValueError("Failed to instantiate queue class '%s': %s",
                             self.queue_cls, e)
        df_cls = load_object(self.dupefilter_cls)
        if hasattr(df_cls, 'from_spider'):
            self.df = load_object(self.dupefilter_cls).from_spider(spider)
        elif hasattr(df_cls, 'from_crawler'):
            self.df = load_object(self.dupefilter_cls).from_crawler(spider.crawler)
        else:
            self.df = load_object(self.dupefilter_cls).from_settings(spider.settings)
        if self.flush_on_start:
            self.flush()
        if self.merge_error_on_start:
            self.queue.shovel()

    def flush(self):
        self.queue.clear()

    def close(self, reason):
        if not self.server.is_closed:
            self.server.close()
            logger.info('关闭rabbitmq连接.')
        self.df.close('关闭rabbitmq连接.')

    def enqueue_request(self, request):
        """
        将程序运行过程中生成的request对象存入队列
        """
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/rabbitmq', spider=self.spider)
        self.queue.push(request)
        return True

    def next_request(self):
        """从队列中取request对象"""
        request = self.queue.pop()
        if not request:
            return
        if self.stats:
            self.stats.inc_value('scheduler/dequeued/rabbitmq',
                                 spider=self.spider)
        return request

    def has_pending_requests(self):
        return len(self.queue)


