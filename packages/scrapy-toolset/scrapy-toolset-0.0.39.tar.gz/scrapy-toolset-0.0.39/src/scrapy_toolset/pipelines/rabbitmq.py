# -*- coding:utf-8 -*-
"""
@desc: 
"""
import importlib
import traceback
from logging import getLogger

import pika
from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings

from scrapy_toolset.scrapy_rabbitmq_scheduler.connection import get_rabbit_from_settings
from scrapy_toolset.scrapy_rabbitmq_scheduler.spiders import RabbitMQListSpider
from scrapy_toolset.scrapy_rabbitmq_scheduler import defaults
from scrapy_toolset.items import RabbitmqItem, RabbitmqBatchItem, RabbitmqTransactionItem
from scrapy_toolset.tools import str_to_bytes

logger = getLogger(__name__)


class RabbitMQPipeline:
    """
    将item存储至rabbitmq
    目前是将list爬虫产生的东西放入detail的start_urls队列中
    """

    def __init__(self, settings: Settings, base_routing_key, serializer, encoding):
        self.client = get_rabbit_from_settings(settings=settings)  # 获取rabbitmq连接
        self.exchange = settings.get('RABBITMQ_EXCHANGE') or defaults.RABBITMQ_EXCHANGE
        self.base_routing_key = base_routing_key
        self.serializer = serializer
        self.encoding = encoding

    @classmethod
    def from_crawler(cls, crawler):
        # 非 RabbitMQListSpider 爬虫不开启此中间件
        if not isinstance(crawler.spider, RabbitMQListSpider):
            raise NotConfigured
        settings = crawler.settings
        spider_name = crawler.spider.name
        base_routing_key = getattr(crawler.spider, "routing_key", None) or defaults.START_URLS_KEY % {
            "spider": spider_name[:-5] + "_detail"}
        serializer_cls = getattr(crawler.spider, 'serializer_cls', None) or defaults.START_URL_SERIALIZER
        serializer = importlib.import_module(serializer_cls)
        encoding = getattr(crawler.spider, 'serializer_encoding', None) or settings.get(
            'START_URL_ENCODING') or defaults.START_URL_ENCODING
        return cls(settings=settings, base_routing_key=base_routing_key, serializer=serializer, encoding=encoding)

    def process_item(self, item, spider):
        return self._process_item(item, spider)

    def _process_item(self, item, spider):
        if isinstance(item, RabbitmqItem):
            self._single_push(item)
        elif isinstance(item, RabbitmqBatchItem):
            self._batch_push(item)
        elif isinstance(item, RabbitmqTransactionItem):
            self._tx_push(item)

        return item

    def _single_push(self, item):
        channel = self.client.channel()
        routing_key = item.get('routing_key') or self.base_routing_key
        channel.basic_publish(exchange=self.exchange,
                              routing_key=routing_key,
                              body=self._get_body(item['data']),
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              )
                              )
        channel.close()

    def _batch_push(self, item):
        channel = self.client.channel()
        routing_key = item.get('routing_key') or self.base_routing_key
        for data in item['datas']:
            channel.basic_publish(exchange=self.exchange,
                                  routing_key=routing_key,
                                  body=self._get_body(data),
                                  properties=pika.BasicProperties(
                                      delivery_mode=2
                                  )
                                  )
        channel.close()

    def _tx_push(self, item):
        """以事务形式提交"""
        channel = self.client.channel()
        routing_key = item.get('routing_key') or self.base_routing_key
        channel.tx_select()
        try:
            for data in item['datas']:
                channel.basic_publish(exchange=self.exchange,
                                      routing_key=routing_key,
                                      body=self._get_body(data),
                                      properties=pika.BasicProperties(
                                          delivery_mode=2
                                      )
                                      )
            channel.tx_commit()
            channel.close()
        except Exception as e:
            channel.tx_rollback()
            if not channel.is_closed:
                channel.close()
            logger.error(traceback.format_exc())
            raise Exception("rabbitmq pipeline存储出现异常.")

    def _get_body(self, data):
        return str_to_bytes(s=self.serializer.dumps(data), encoding=self.encoding)

    def close_spider(self, spider):
        self.client.close()
