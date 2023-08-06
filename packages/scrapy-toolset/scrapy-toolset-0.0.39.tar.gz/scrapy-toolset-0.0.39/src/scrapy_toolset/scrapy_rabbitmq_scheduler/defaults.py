import pika
from scrapy.exceptions import IgnoreRequest
# rabbitmq-plugins enable rabbitmq_shovel
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = None
RABBITMQ_PASSWORD = None
RABBITMQ_MANAGEMENT_PORT = 15672
RABBITMQ_MANAGEMENT_SCHEME = 'http'
RABBITMQ_HEARTBEAT = 1800
RABBITMQ_CREDENTIALS = ()
RABBITMQ_VIRTUAL_HOST = '/'
RABBITMQ_EXCHANGE = 'scrapy_rabbitmq_exchange'
RABBITMQ_PARAMETERS = {

}
RABBITMQ_QUEUE_ARGUMENTS = {

}
# 队列类,
SCHEDULER_QUEUE_CLASS = 'scrapy_toolset.scrapy_rabbitmq_scheduler.queue.FifoQueue'

# start_urls队列名称
SPIDER_START_URLS_QUEUE = '%(spider)s:start_urls'
# 请求队列名称
SCHEDULER_REQUESTS_QUEUE = '%(spider)s:requests'
# 错误队列名称
SCHEDULER_ERROR_QUEUE = "%(spider)s:requests:error"
# 持久化队列
SCHEDULER_PERSIST = True
# 消息确认
SCHEDULER_AUTOACK = False
# 启动时删除队列
SCHEDULER_FLUSH_ON_START = False
# 启动时合并错误队列
SCHEDULER_MERGE_ERROR_ON_START = False
# 无请求时，最大等待时间
MAX_IDLE_TIME_BEFORE_CLOSE = 0
# 序列化器类
SCHEDULER_SERIALIZER = 'scrapy_toolset.scrapy_rabbitmq_scheduler.picklecompat'
# 爬虫start_urls序列化器
START_URL_SERIALIZER = 'json'
# 从start_urls队列中取的数据的编码
START_URL_ENCODING = 'utf-8'
# 为True时，发送消息确认， 为False时，发送nack 将消息发送至error队列
# item流经pipelines时被drop，是否ack消息
SCHEDULER_ACK_ON_ITEM_DROPPED = False
# item流经pipelines时出现异常，是否ack消息
SCHEDULER_ACK_ON_ITEM_ERROR = False
# 由于当前消息确认都与item相关，但如果没有产生item, 则默认在spider middleware的process_spider_output结束时ack消息
SCHEDULER_ACK_ON_ITEM_NOT_GENERATED = True
# 当请求进入失败逻辑，需要进入错误队列时，需要将哪个请求放入错误队列
SCHEDULER_REQUEUE_ORIGIN_REQUEST = False
# start_urls队列ack逻辑
SCHEDULER_IGNORE_EXCEPTIONS = [IgnoreRequest, ]

