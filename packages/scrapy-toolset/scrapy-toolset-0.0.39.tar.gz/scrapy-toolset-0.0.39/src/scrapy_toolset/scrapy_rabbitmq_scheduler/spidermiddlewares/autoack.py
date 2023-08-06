# -*- coding:utf-8 -*-
"""
@desc: 
"""
from logging import getLogger
from itemadapter import is_item
from scrapy import Request
from scrapy.exceptions import NotConfigured
from scrapy.utils.misc import load_object
from scrapy import signals
from ..scheduler import Scheduler

logger = getLogger(__name__)


class AutoAckMiddleware:
    """
    由于scheduler的消息确认逻辑与item息息相关，当爬虫解析函数执行完毕并未产生item时，该消息将一直处于unack状态
    为了避免以上情况，使用此中间件对未产生item的请求进行自动确认或requeue至错误队列
    """

    def __init__(self, settings):
        self.auto_ack = settings.get('SCHEDULER_ACK_ON_ITEM_NOT_GENERATED', True)
        self.origin_requeue = settings.get("SCHEDULER_REQUEUE_ORIGIN_REQUEST", False)
        self.ack_on_item_error = settings.getbool('SCHEDULER_ACK_ON_ITEM_ERROR')
        self.ack_on_item_dropped = settings.getbool('SCHEDULER_ACK_ON_ITEM_DROPPED')
        scheduler_cls = load_object(settings.get('SCHEDULER'))
        if not issubclass(scheduler_cls, Scheduler):
            raise NotConfigured

    @classmethod
    def from_settings(cls, settings):
        return cls(settings=settings)

    @classmethod
    def from_crawler(cls, crawler):
        instance = cls.from_settings(crawler.settings)
        instance.stats = crawler.stats
        crawler.signals.connect(instance.request_dropped, signals.request_dropped)
        crawler.signals.connect(instance.response_downloaded, signals.response_downloaded)
        crawler.signals.connect(instance.spider_error, signals.spider_error)
        crawler.signals.connect(instance.item_scraped, signals.item_scraped)
        crawler.signals.connect(instance.item_dropped, signals.item_dropped)
        crawler.signals.connect(instance.item_error, signals.item_error)
        return instance

    def process_spider_output(self, response, result, spider):
        item_generated, list_result = False, []
        item_count = 0
        for i in result:
            # 记录是否生成过item以实现根据配置在爬虫未解析出item时进行ack
            if is_item(i):
                item_generated = True
                item_count += 1
            # 根据配置为请求添加起始request对象字段
            if self.origin_requeue:
                if isinstance(i, Request):
                    depth = response.request.meta.get("depth")
                    # start_urls产生的请求对应的响应
                    if depth == 0:
                        i.meta['_origin_request'] = response.request
                    elif depth >= 1:
                        i.meta['_origin_request'] = response.meta.get("_origin_request")
            list_result.append(i)
        response.request.meta['_item_count'] = item_count
        # 为当前请求添加一个字段以记录该请求产生了多少个item
        for i in list_result:
            yield i

        if not item_generated:
            if self.auto_ack and not response.meta.get('dont_auto_ack'):
                spider.logger.debug(
                    '当前请求未产生ITEM， 根据配置，已自动ACK:{}， 如果希望关闭此功能请配置SCHEDULER_ACK_ON_ITEM_NOT_GENERATED=False 或在meta中添加dont_auto_ack=True'.format(
                        response.request))
                spider.crawler.engine.slot.scheduler.queue.ack(request=response.request)
            else:
                spider.crawler.engine.slot.scheduler.queue.nack(request=response.request, requeue=False)


    def response_downloaded(self, response, request, spider):
        # 重定向请求需要单独处理一下
        allowed_status = (301, 302, 303, 307, 308)
        if not ('Location' not in response.headers or response.status not in allowed_status):
            spider.crawler.engine.slot.scheduler.queue.ack(request=request)

    def request_dropped(self, request, spider):
        """丢弃请求时，发送消息确认以删除该消息， 一般发生在该请求被过滤时"""
        spider.crawler.engine.slot.scheduler.queue.ack(request=request)

    def item_scraped(self, item, response, spider):
        """
            item流经所有pipeline，可以确定该请求已经完毕，发送消息确认以删除该消息
            当一个请求产生多个item时，为保证item都存储成功，可以在meta中添加 _item_count 参数来指定有多少个item
        """
        _item_count = response.request.meta.get("_item_count")
        success_count = response.request.meta.get("_success_count") or 1
        if success_count >= _item_count:
            spider.crawler.engine.slot.scheduler.queue.ack(request=response.request)
        else:
            response.request.meta['_success_count'] = success_count + 1

    def spider_error(self, failure, response, spider):
        """解析函数异常时，将消息发送至error"""
        spider.crawler.engine.slot.scheduler.queue.nack(request=response.request)
        logger.error(
            'spider parse function failure, request url:%s,request has been published error queue.' % response.url)
        logger.exception(failure)

    def item_dropped(self, item, response, spider):
        """根据配置决定确认与否"""
        if self.ack_on_item_dropped:
            logger.error(
                'item_dropped，item from:%s, request message has acked, if you dont want do this , set SCHEDULER_ACK_ON_ITEM_DROPPED=False.' % response.url)
            spider.crawler.engine.slot.scheduler.queue.ack(request=response.request)
        else:
            logger.error(
                'item_dropped，item from:%s, request has been published error queue, if you dont want do this , set SCHEDULER_ACK_ON_ITEM_DROPPED=True.' % response.url)
            spider.crawler.engine.slot.scheduler.queue.nack(request=response.request)

    def item_error(self, item, spider, response):
        """根据配置决定确认与否"""
        if self.ack_on_item_error:
            logger.error(
                'item_error，item from:%s, request message has acked, if you dont want do this , set SCHEDULER_ACK_ON_ITEM_ERROR=False.' % response.url)
            spider.crawler.engine.slot.scheduler.queue.ack(request=response.request)
        else:
            logger.error(
                'item_error，item from:%s, request has been published error queue, if you dont want do this , set SCHEDULER_ACK_ON_ITEM_ERROR=True.' % response.url)
            spider.crawler.engine.slot.scheduler.queue.nack(request=response.request)
