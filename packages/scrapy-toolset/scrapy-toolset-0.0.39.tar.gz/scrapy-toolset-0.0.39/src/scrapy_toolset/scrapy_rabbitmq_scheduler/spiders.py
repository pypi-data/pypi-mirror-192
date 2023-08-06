# -*- coding:utf-8 -*-
"""
@desc: 
"""
import importlib
import time
import uuid

from scrapy import signals, Request
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider

from scrapy.utils.misc import load_object
from . import connection, defaults
from .downloadermiddlewares.retry import RetryMiddleware
from .spidermiddlewares.autoack import AutoAckMiddleware
from .utils import AttributeDict


class ParamsMinin(object):
    redis_bloom_version = 'v1'  # 布隆过滤器版本号后缀
    redis_bloom_clear = True  # 清除之前的版本号


class RabbitMQMixin(object):
    """Mixin class to implement reading urls from a redis queue."""
    name = None
    start_urls_routing_key = None
    crawler = None
    settings = None
    use_start_urls = True
    spider_idle_start_time = int(time.time())
    start_urls = []
    batch_size = 1
    start_url_encoding = 'utf-8'

    def setup(self, crawler):
        if crawler is None:
            crawler = getattr(self, 'crawler', None)
        if crawler is None:
            raise ValueError("crawler is required")
        settings = crawler.settings
        serializer = settings.get('START_URL_SERIALIZER') or defaults.START_URL_SERIALIZER
        self.start_url_encoding = settings.get('START_URL_ENCODING') or defaults.START_URL_ENCODING
        self.batch_size = settings.getint('CONCURRENT_REQUESTS')
        if self.scheduler_starturls_key is None:
            self.start_urls_routing_key = settings.get('SCHEDULER_STARTURLS_KEY', defaults.SCHEDULER_STARTURLS_KEY) % {
                'spider': self.name}
        elif not self.start_urls_routing_key.strip():
            raise ValueError("routing key must not be empty")

        self.scheduler_routing_keys = {
            # start_urls队列
            "start_urls": self.start_urls_routing_key,
            # 请求队列
            "requests": (settings.get('SCHEDULER_QUEUE_KEY') or defaults.SCHEDULER_QUEUE_KEY) % {'spider': self.name},
            # 错误队列
            "errors": (settings.get('SCHEDULER_ERROR_QUEUE_KEY') or defaults.SCHEDULER_QUEUE_KEY) % {
                'spider': self.name}
        }
        queue_cls = load_object(self.settings.get('SCHEDULER_QUEUE_CLASS') or defaults.SCHEDULER_QUEUE_CLASS)
        queue = queue_cls(spider=self, key=self.start_urls_routing_key,
                          serializer=importlib.import_module(serializer))
        # 声明队列
        queue.queue_init(self.scheduler_routing_keys)
        # todo 如果是列表页爬虫，声明详情页队列
        if isinstance(self, RabbitMQListSpider):
            # 去掉_list + _detail
            if not self.name.endswith("_list"):
                raise ValueError("RabbitMQListSpider爬虫必须以 _list 结尾")
            detail_name = self.name[:-5] + "_detail"
            routing_keys = {
                # start_urls队列
                "start_urls": (settings.get('START_URLS_KEY') or defaults.START_URLS_KEY) % {
                    'spider': detail_name},
                # 请求队列
                "requests": (settings.get('SCHEDULER_QUEUE_KEY') or defaults.SCHEDULER_QUEUE_KEY) % {
                    'spider': detail_name},
                # 错误队列
                "errors": (settings.get('SCHEDULER_ERROR_QUEUE_KEY') or defaults.SCHEDULER_ERROR_QUEUE_KEY) % {
                    'spider': detail_name}
            }
            queue.queue_init(routing_keys)

        self.queue = queue
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(self.request_scheduled, signal=signals.request_scheduled)
        crawler.signals.connect(self.request_dropped, signal=signals.request_dropped)

    def request_scheduled(self, request, spider):
        """通过start_url生成的请求到达调度器时，发送消息确认"""
        self.queue.ack(request=request, is_start_url=True)

    def request_dropped(self, request, spider):
        """通过start_urls取出的数据生成的请求被过滤或主动抛弃"""
        self.queue.ack(request=request, is_start_url=True)

    def start_requests(self):
        """
        返回一个迭代器，以遍历rabbitmq队列
        当启动时发现队列为空时，获取爬虫start_urls，将其放入rabbitmq中的spider:start_urls队列

        如果不想将start_urls存入队列，此方法只留存一个yield即可
        """
        if getattr(self, 'use_start_urls', True):
            for start_url in self.start_urls:
                request = self.make_requests_from_url(start_url)
                yield request

    def next_requests(self):
        """
        Returns a request to be scheduled or none.
        需要支持先把start_urls内的数据放入队列，但如果start_urls量很多，如果同步进行，将会阻塞相当长的一段时间，需要特殊处理，在这里使用yield from
        """
        msgs = list(self.queue.fetch(batch_size=self.batch_size, raw=True))
        for msg in msgs:
            if msg:
                body, channel = msg
                request = self.make_requests_from_url(body)
                start_rabbitmq_channel_id = uuid.uuid4().__str__()
                request.meta['start_rabbitmq_channel_id'] = start_rabbitmq_channel_id
                self.queue.channel_pool[start_rabbitmq_channel_id] = channel
                yield request

    def schedule_next_requests(self):
        """Schedules a request if available"""
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def make_requests_from_url(self, url) -> Request:
        raise NotImplementedError

    def spider_idle(self):
        """
        Schedules a request if available, otherwise waits.
        or close spider when waiting seconds > MAX_IDLE_TIME_BEFORE_CLOSE.
        MAX_IDLE_TIME_BEFORE_CLOSE will not affect SCHEDULER_IDLE_BEFORE_CLOSE.
        """
        if self.rabbitmq_connection is not None and len(self.queue) > 0:
            self.spider_idle_start_time = int(time.time())

        self.schedule_next_requests()

        max_idle_time = self.settings.getint("MAX_IDLE_TIME_BEFORE_CLOSE")
        idle_time = int(time.time()) - self.spider_idle_start_time
        if max_idle_time != 0 and idle_time >= max_idle_time:
            return
        raise DontCloseSpider


class RabbitMQspider(Spider, RabbitMQMixin, ParamsMinin):

    @classmethod
    def update_settings(cls, settings):
        super(RabbitMQspider, cls).update_settings(settings=settings)
        settings.setdict(cls.custom_settings or {}, priority='spider')
        # 自动加载两个中间件，也可以手动加载
        retry_middleware = RetryMiddleware.__module__ + '.' + RetryMiddleware.__name__
        auto_ack_middleware = AutoAckMiddleware.__module__ + '.' + AutoAckMiddleware.__name__
        # 需要比原retry middleware权值大一点
        priority = settings['DOWNLOADER_MIDDLEWARES'].get("scrapy.downloadermiddlewares.retry.RetryMiddleware") or 999
        settings['DOWNLOADER_MIDDLEWARES'][retry_middleware] = priority + 100
        if not settings['SPIDER_MIDDLEWARES'].get(auto_ack_middleware):
            settings['SPIDER_MIDDLEWARES'][auto_ack_middleware] = 999

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = super(RabbitMQspider, self).from_crawler(crawler, *args, **kwargs)
        obj.setup(crawler)
        return obj


class RabbitMQListSpider:
    name = None  # 爬虫名，要以 _list 结尾，那样的话，会自动发送至_detail结尾的爬虫的start_urls队列
    serializer_cls = None  # 序列化器类，默认是使用json  对应配置项:START_URL_SERIALIZER
    serializer_encoding = None  # 如果序列化之后不是bytes类型，编码类型, 对应配置项:START_URL_ENCODING
    routing_key = None  # 发送至哪个队列，会自动根据爬虫名配置，可以不填，队列名的获取顺序为 1.item中指定 2.spider.routing_key 3.根据爬虫名拼接
