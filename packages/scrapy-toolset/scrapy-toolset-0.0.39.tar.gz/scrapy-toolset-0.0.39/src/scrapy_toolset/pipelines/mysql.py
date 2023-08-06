# -*- coding:utf-8 -*-
"""
@desc: 
"""
import traceback

from scrapy.exceptions import DropItem
from twisted.internet.threads import deferToThread

from scrapy_toolset.items import (MysqlItem,
                                  MysqlInsertItem,
                                  MysqlUpdateItem,
                                  MysqlBatchItem)
from scrapy_toolset.connection import get_mysql_connection
from scrapy_toolset.tools import make_insert_sql, make_batch_sql, make_update_sql


class MysqlPipeline(object):

    def __init__(self, client):
        self.client = client

    @classmethod
    def from_settings(cls, settings):
        return cls(client=get_mysql_connection(settings=settings))


    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        if isinstance(item, MysqlItem):
            sql, values = self.make_sql(item)
            self.save(sql=sql, values=values)
        return item

    def save(self, sql, values=None):
        conn = self.client.connection()
        cursor = conn.cursor()
        try:
            if values:
                cursor.executemany(sql, values)
            else:
                cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            cursor.close()
            conn.close()
            raise DropItem

    def make_sql(self, item):
        values = None
        if isinstance(item, MysqlInsertItem):
            sql = make_insert_sql(**item)
        elif isinstance(item, MysqlUpdateItem):
            sql = make_update_sql(**item)
        elif isinstance(item, MysqlBatchItem):
            sql, values = make_batch_sql(**item)
        else:
            raise TypeError('未知的item类型')
        return sql, values
