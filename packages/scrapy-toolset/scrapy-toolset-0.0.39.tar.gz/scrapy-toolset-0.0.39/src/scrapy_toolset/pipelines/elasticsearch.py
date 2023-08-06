# -*- coding:utf-8 -*-
"""
@desc: 
"""
import logging

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from scrapy.exceptions import NotConfigured, DropItem
from twisted.internet.threads import deferToThread

from scrapy_toolset.items import (ElasticsearchInsertItem,
                                  ElasticsearchBulkItem,
                                  ElasticsearchBulkActionItem)
from scrapy_toolset.tools import make_actions


class ElasticsearchPipeline(object):

    def __init__(self, settings):
        hosts = settings.get('ELASTICSEARCH_HOSTS')
        if not hosts:
            logging.getLogger(__name__).warning('未配置ELASTICSEARCH_HOSTS')
            raise NotConfigured
        username = settings.get('ELASTICSEARCH_USERNAME')
        password = settings.get('ELASTICSEARCH_PASSWORD')
        timeout = settings.getint('ELASTICSEARCH_TIMEOUT', 300)

        if all([username, password]):
            http_auth = (username, password)
        else:
            http_auth = None
        self.client = Elasticsearch(hosts=hosts, http_auth=http_auth, timeout=timeout)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        if isinstance(item, ElasticsearchInsertItem):
            self.client.index(**item)
        elif isinstance(item, ElasticsearchBulkItem):
            actions = make_actions(**item)
            bulk(self.client, actions=actions)
        elif isinstance(item, ElasticsearchBulkActionItem):
            actions = item['actions']
            if actions:
                bulk(self.client, actions=actions)
        return item





