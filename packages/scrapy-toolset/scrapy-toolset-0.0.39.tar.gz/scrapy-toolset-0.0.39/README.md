============
scrapy-toolset
============

Installing

```
$ pip install git+https://gitee.com/lambdajing/scrapy-toolset.git --upgrade
```


## rabbitmq scheduler usage
执行此命令以支持错误队列合并
`rabbitmq-plugins enable rabbitmq_shovel`
```python

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_MANAGEMENT_PORT = 15672
RABBITMQ_MANAGEMENT_SCHEME = 'http'
RABBITMQ_HEARTBEAT = 3600
RABBITMQ_CLS = pika.BlockingConnection
RABBITMQ_CREDENTIALS = ('guest', 'guest')
RABBITMQ_VIRTUAL_HOST = '/'
RABBITMQ_EXCHANGE = 'scrapy_rabbitmq_exchange'
RABBITMQ_PARAMETERS = {
    'host': RABBITMQ_HOST,
    'port': RABBITMQ_PORT,
    'credentials': RABBITMQ_CREDENTIALS,
    'virtual_host': RABBITMQ_VIRTUAL_HOST,
    'heartbeat': RABBITMQ_HEARTBEAT,
}
RABBITMQ_QUEUE_ARGUMENTS = {

}

SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
RABBITMQ_START_URLS_KEY = '%(spider)s:start_urls'
# 持久化队列
SCHEDULER_PERSIST = True
# 消息确认
SCHEDULER_AUTOACK = False
# 启动时删除队列
SCHEDULER_FLUSH_ON_START = False
# 启动时合并错误队列
SCHEDULER_MERGE_ERROR_ON_START = False
# 队列类,
SCHEDULER_QUEUE_CLASS = 'scrapy_toolset.scrapy_rabbitmq_scheduler.queue.FifoQueue'
# 无请求时，最大等待时间
MAX_IDLE_TIME_BEFORE_CLOSE = 0
# 序列化器类
SCHEDULER_SERIALIZER = 'scrapy_toolset.scrapy_rabbitmq_scheduler.picklecompat'
# item存储失败时，即触发 item_dropped 和 item_error时 应作何处理
# 为True时，发送消息确认， 为False时，发送nack 将消息发送至error队列
SCHEDULER_ACK_ON_ITEM_DROPPED = False
SCHEDULER_ACK_ON_ITEM_ERROR = False

# request对象主动ack添加
# 针对没有产生item地请求，可通过以下方式进行ack
```
## elasticsearch pipeline settings
```
ELASTICSEARCH_HOSTS
ELASTICSEARCH_USERNAME
ELASTICSEARCH_PASSWORD
ELASTICSEARCH_TIMEOUT
```

## mongodb pipeline
```
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_USERNAME = ""
MONGODB_PASSWORD = "password"
MONGODB_AUTHSOURCE = "admin"

# 参考items实现
item = MongoItem()
item['db'] = "tokenview"
item['table'] = "data"
item['data'] = {"_id":"xxx", "name":"xxx"}
item['filter_columns'] = ("_id", ) # 过滤条件字段, 不填话会去data里找_id
item['update_columns'] = ("name", ) # 重复的时候，要更新的字段
item['auto_update'] = False # 直接覆盖插入

item = MongoBatchItem()
item['db'] = "tokenview"
item['table'] = "data"
item['filter_columns'] = ("txid",)
item['update_columns'] = ("name", )
for index,i in enumerate(data['data']):
    i['name'] = index
item['datas'] = data['data']
yield item
```
