# -*- coding:utf-8 -*-
"""
@desc: 
"""
from twisted.internet.threads import deferToThread

from scrapy_toolset.items import (BaseMongoItem,
                                  MongoItem,
                                  MongoBatchItem)
from scrapy_toolset.connection import get_mongodb_connection
from scrapy_toolset.tools import make_mongo_action, make_mongo_batch_action


class MongodbPipeline(object):

    def __init__(self, settings):
        self.client = get_mongodb_connection(settings=settings)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        if isinstance(item, BaseMongoItem):
            db = self.client.get_database(item['db'])
            collection = db.get_collection(item['table'])
            if isinstance(item, MongoItem):
                actions = [make_mongo_action(**item),]
            elif isinstance(item, MongoBatchItem):
                actions = make_mongo_batch_action(**item)
            else:
                # 自定义item, actions直接保存为字段
                actions = item['actions']
            collection.bulk_write(actions)
        return item
