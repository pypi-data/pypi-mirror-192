# -*- coding:utf-8 -*-
"""
@desc: 
"""
import scrapy


class BaseElasticsearchItem(scrapy.Item):
    def __setitem__(self, key, value):
        self._values[key] = value


class ElasticsearchInsertItem(BaseElasticsearchItem):
    index = scrapy.Field()
    doc_type = scrapy.Field()
    document = scrapy.Field()
    body = scrapy.Field()
    id = scrapy.Field()


class ElasticsearchBulkItem(BaseElasticsearchItem):
    index = scrapy.Field()
    doc_type = scrapy.Field()
    id_column = scrapy.Field()  # 主键字段
    datas = scrapy.Field()
    auto_update = scrapy.Field()  # 采集index进行， 默认为False
    update_columns = scrapy.Field()  # 重复时更新字段
    params = scrapy.Field()  # 额外参数


class ElasticsearchBulkActionItem(BaseElasticsearchItem):
    actions = scrapy.Field()


class MysqlItem(scrapy.Item):
    pass


class MysqlInsertItem(MysqlItem):
    """mysql 单条插入item"""
    table = scrapy.Field()  # 表名
    data = scrapy.Field()  # 数据
    auto_update = scrapy.Field()  # 是否采用replace into
    update_columns = scrapy.Field()  # 重复时更新字段
    insert_ignore = scrapy.Field()  # 忽略失败的


class MysqlUpdateItem(MysqlItem):
    """mysql 更新item"""
    table = scrapy.Field()  # 表名
    data = scrapy.Field()  # 数据
    condition = scrapy.Field()  # 更新条件 直接字符串


class MysqlBatchItem(MysqlItem):
    """mysql 批量操作item"""
    table = scrapy.Field()  # 表名
    datas = scrapy.Field()  # 数据
    auto_update = scrapy.Field()  # 是否采用replace into
    update_columns = scrapy.Field()  # 重复时更新字段
    update_columns_value = scrapy.Field()  # 重复时更新值


class BaseMongoItem(scrapy.Item):
    actions = scrapy.Field()


class MongoItem(BaseMongoItem):
    db = scrapy.Field()
    table = scrapy.Field()
    id = scrapy.Field()
    filter_columns = scrapy.Field()
    data = scrapy.Field()
    auto_update = scrapy.Field()  # 是否采用ReplaceOne
    update_columns = scrapy.Field()


class MongoBatchItem(BaseMongoItem):
    db = scrapy.Field()
    table = scrapy.Field()
    datas = scrapy.Field()
    filter_columns = scrapy.Field()
    auto_update = scrapy.Field()  # 是否采用ReplaceOne
    update_columns = scrapy.Field()


# rabbitmq相关item
class RabbitmqItem(scrapy.Item):
    routing_key = scrapy.Field()
    data = scrapy.Field()


class RabbitmqBatchItem(scrapy.Item):
    """批量发送，其实跟单个发送区别不太大"""
    routing_key = scrapy.Field()
    datas = scrapy.Field()


class RabbitmqTransactionItem(scrapy.Item):
    """以事务形式进行消息发送"""
    routing_key = scrapy.Field()
    datas = scrapy.Field()


if __name__ == '__main__':
    a = MongoBatchItem()
