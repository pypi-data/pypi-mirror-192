# -*- coding:utf-8 -*-
"""
@desc: 
"""
from logging import getLogger, Logger
from typing import Optional, Union

from scrapy.utils.misc import load_object
from twisted.internet import defer
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)
from twisted.web.client import ResponseFailed

from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.exceptions import NotConfigured
from scrapy.http.request import Request
from scrapy.spiders import Spider
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message

from ..scheduler import Scheduler
from .. import defaults

retry_logger = getLogger(__name__)


def get_request_on_failure(request):
    father_request = request.meta.get("father_request")
    if father_request:
        return father_request
    else:
        new_request = request.copy()
        new_request.meta['retry_times'] = 0
        return new_request


def get_retry_request(
        request: Request,
        *,
        spider: Spider,
        reason: Union[str, Exception] = 'unspecified',
        max_retry_times: Optional[int] = None,
        priority_adjust: Optional[int] = None,
        logger: Logger = retry_logger,
        stats_base_key: str = 'retry',
):
    """
    Returns a new :class:`~scrapy.Request` object to retry the specified
    request, or ``None`` if retries of the specified request have been
    exhausted.

    For example, in a :class:`~scrapy.Spider` callback, you could use it as
    follows::

        def parse(self, response):
            if not response.text:
                new_request_or_none = get_retry_request(
                    response.request,
                    spider=self,
                    reason='empty',
                )
                return new_request_or_none

    *spider* is the :class:`~scrapy.Spider` instance which is asking for the
    retry request. It is used to access the :ref:`settings <topics-settings>`
    and :ref:`stats <topics-stats>`, and to provide extra logging context (see
    :func:`logging.debug`).

    *reason* is a string or an :class:`Exception` object that indicates the
    reason why the request needs to be retried. It is used to name retry stats.

    *max_retry_times* is a number that determines the maximum number of times
    that *request* can be retried. If not specified or ``None``, the number is
    read from the :reqmeta:`max_retry_times` meta key of the request. If the
    :reqmeta:`max_retry_times` meta key is not defined or ``None``, the number
    is read from the :setting:`RETRY_TIMES` setting.

    *priority_adjust* is a number that determines how the priority of the new
    request changes in relation to *request*. If not specified, the number is
    read from the :setting:`RETRY_PRIORITY_ADJUST` setting.

    *logger* is the logging.Logger object to be used when logging messages

    *stats_base_key* is a string to be used as the base key for the
    retry-related job stats
    """
    settings = spider.crawler.settings
    stats = spider.crawler.stats
    retry_times = request.meta.get('retry_times', 0) + 1
    if max_retry_times is None:
        max_retry_times = request.meta.get('max_retry_times')
        if max_retry_times is None:
            max_retry_times = settings.getint('RETRY_TIMES')
    if retry_times <= max_retry_times:
        logger.debug(
            "Retrying %(request)s (failed %(retry_times)d times): %(reason)s",
            {'request': request, 'retry_times': retry_times, 'reason': reason},
            extra={'spider': spider}
        )
        new_request = request.copy()
        new_request.meta['retry_times'] = retry_times
        new_request.dont_filter = True
        if priority_adjust is None:
            priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        new_request.priority = request.priority + priority_adjust

        if callable(reason):
            reason = reason()
        if isinstance(reason, Exception):
            reason = global_object_name(reason.__class__)

        stats.inc_value(f'{stats_base_key}/count')
        stats.inc_value(f'{stats_base_key}/reason_count/{reason}')
        # 将当前请求删除，以新的请求进行替换
        if hasattr(spider.crawler.engine.slot.scheduler.queue, 'ack'):
            spider.crawler.engine.slot.scheduler.queue.ack(request=request)

        return new_request
    else:
        # 重试达到上限，如果直接进行nack,那么下次取到的仍然是重试达到上限的请求
        if hasattr(spider.crawler.engine.slot.scheduler.queue, 'nack'):
            new_request = request.copy()
            new_request.meta['retry_times'] = 0
            spider.crawler.engine.slot.scheduler.queue.nack(request=request, requeue=False, replace_request=new_request)
            logger.debug(
                "Gave up retrying %(request)s (failed %(retry_times)d times): "
                "%(reason)s and send request to error requeue: replace_request:%(replace_request)s",
                {'request': request, 'retry_times': retry_times, 'reason': reason, "replace_request": new_request},
                extra={'spider': spider},
            )
        else:
            logger.error(
                "Gave up retrying %(request)s (failed %(retry_times)d times): "
                "%(reason)s",
                {'request': request, 'retry_times': retry_times, 'reason': reason},
                extra={'spider': spider},
            )
        stats.inc_value(f'{stats_base_key}/max_reached')

        return None


class RetryMiddleware:
    # IOError is raised by the HttpCompression middleware when trying to
    # decompress an empty response
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError)

    def __init__(self, settings):
        # 需要满足开启重试以及请求队列是基于rabbitmq
        self.retry_enable = settings.getbool('RETRY_ENABLED')
        scheduler_cls = load_object(settings.get('SCHEDULER'))
        if not issubclass(scheduler_cls, Scheduler):
            retry_logger.info(
                'close rabbitmq scheduler retry middlerware because of scheduler_cls:{scheduler_cls} is not subclass of SCHEDULER'.format(
                    scheduler_cls=settings.get('SCHEDULER')))
            raise NotConfigured

        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        self.ignore_exceptions = tuple(settings.getlist('SCHEDULER_IGNORE_EXCEPTIONS') + defaults.SCHEDULER_IGNORE_EXCEPTIONS)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if self.retry_enable:
            if request.meta.get('dont_retry', False):
                return response
            if response.status in self.retry_http_codes:
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and self.retry_enable:
            if request.meta.get('dont_retry', False):
                return self._retry(request, exception, spider)
            else:
                if hasattr(spider.crawler.engine.slot.scheduler.queue, 'nack'):
                    spider.crawler.engine.slot.scheduler.queue.nack(request=request, requeue=False)
        else:
            # 非重试性错误, 直接扔了
            if isinstance(exception, self.ignore_exceptions):
                retry_logger.error(
                    "ignore exception occurs %(request)s  "
                    "%(reason)s, drop current request",
                    {'request': request, 'reason': exception},
                    extra={'spider': spider},
                )
                if hasattr(spider.crawler.engine.slot.scheduler.queue, 'ack'):
                    spider.crawler.engine.slot.scheduler.queue.ack(
                        request=request)
            else:
                retry_logger.error(
                    "dont retry exception occurs %(request)s  "
                    "%(reason)s, send request to error queue",
                    {'request': request, 'reason': exception},
                    extra={'spider': spider},
                )
                if hasattr(spider.crawler.engine.slot.scheduler.queue, 'nack'):
                    spider.crawler.engine.slot.scheduler.queue.nack(request=request, requeue=False)

    def _retry(self, request, reason, spider):
        max_retry_times = request.meta.get('max_retry_times', self.max_retry_times)
        priority_adjust = request.meta.get('priority_adjust', self.priority_adjust)
        return get_retry_request(
            request,
            reason=reason,
            spider=spider,
            max_retry_times=max_retry_times,
            priority_adjust=priority_adjust,
        )
