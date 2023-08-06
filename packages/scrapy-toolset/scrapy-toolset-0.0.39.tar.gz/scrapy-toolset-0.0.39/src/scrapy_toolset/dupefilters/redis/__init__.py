# -*- coding:utf-8 -*-
"""
@desc: 
"""
import logging

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from . import defaults
from scrapy_toolset.connection import get_redis_from_settings
from scrapy_toolset.tools import bytes_to_str

logger = logging.getLogger(__name__)
from redis import Redis


# TODO: Rename class to RedisDupeFilter.
class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplicates filter.

    This class can also be used with default Scrapy's scheduler.

    """

    logger = logger

    def __init__(self, server, key, debug=False):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.

        """
        self.server = server
        self.key = key
        self.debug = debug
        self.logdupes = True

    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        added = self.server.sadd(self.key, fp)
        return added == 0

    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    @classmethod
    def from_spider(cls, spider):
        settings = spider.settings
        server = get_redis_from_settings(settings)
        dupefilter_key = settings.get("SCHEDULER_DUPEFILTER_KEY", defaults.SCHEDULER_DUPEFILTER_KEY)
        key = dupefilter_key % {'spider': spider.name}
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, key=key, debug=debug)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        self.server.delete(self.key)

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False
        spider.crawler.stats.inc_value('dupefilter/redis/filtered', spider=spider)

class RBLDupeFilter(BaseDupeFilter):
    """Redis-based request duplicates filter.

        This class can also be used with default Scrapy's scheduler.

        """

    logger = logger

    def __init__(self, server, key, debug=False, persist=True):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.

        """
        self.server: Redis = server
        self.key = key
        self.debug = debug
        self.logdupes = True
        self.persist = persist

    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        added = self.server.execute_command("BF.ADD", self.key, fp)
        return added == 0

    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    @staticmethod
    def initial_filter(server: Redis, key, version, clear, persist=True, error_rate=0.0001, capacity=10000):
        """

        :param server:
        :param key:
        :param version: key版本号
        :param clear: 删除本爬虫历史产生的过滤器
        :param persist: 过滤器持久化
        :param error_rate: 可容忍的错误率
        :param capacity: 过滤器容量，实际元素的数量超过这个初始化容量时，误判率上升。
        :return:
        """
        # 过滤器key
        vkey = '%(key)s:%(version)s' % {"key": key, "version": version}
        # 根据clear和persist清除历史过滤器
        if clear:
            keys: list = server.keys('%(key)s*' % {"key": key})
            if persist:
                for key in keys:
                    if bytes_to_str(key) != vkey:
                        server.delete(key)
            else:
                server.delete(*keys)

        if not server.exists(vkey):
            server.execute_command('BF.RESERVE', vkey, error_rate, capacity)

    @classmethod
    def from_spider(cls, spider):
        settings = spider.settings
        server = get_redis_from_settings(settings)
        dupefilter_key = settings.get("SCHEDULER_DUPEFILTER_KEY", defaults.SCHEDULER_DUPEFILTER_KEY)
        error_rate = settings.get('SCHEDULER_DUPEFILTER_ERROR_RATE', defaults.SCHEDULER_DUPEFILTER_ERROR_RATE)
        capacity = settings.get('SCHEDULER_DUPEFILTER_CAPACITY', defaults.SCHEDULER_DUPEFILTER_CAPACITY)
        persist = settings.get('SCHEDULER_DUPEFILTER_PERSIST', defaults.SCHEDULER_DUPEFILTER_PERSIST)
        key = dupefilter_key % {'spider': spider.name}
        debug = settings.getbool('DUPEFILTER_DEBUG')
        # 版本
        version = getattr(spider, 'redis_bloom_version', 'v1')
        # 清除历史
        clear = getattr(spider, 'redis_bloom_clear', True)
        cls.initial_filter(server=server, key=key, version=version, clear=clear, persist=persist, error_rate=error_rate,
                           capacity=capacity)
        vkey = '%(key)s:%(version)s' % {"key": key, "version": version}
        return cls(server, key=vkey, debug=debug, persist=persist)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        if not self.persist:
            self.clear()

    def clear(self):
        """Clears fingerprints data."""
        try:
            self.server.delete(self.key)
        except:
            pass

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False
        spider.crawler.stats.inc_value('dupefilter/redis_bloom/filtered', spider=spider)
