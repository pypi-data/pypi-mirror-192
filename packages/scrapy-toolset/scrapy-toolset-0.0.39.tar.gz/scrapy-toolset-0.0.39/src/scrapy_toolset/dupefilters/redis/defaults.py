# -*- coding:utf-8 -*-
"""
@desc: 
"""
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# https://cloud.tencent.com/developer/article/1586931
# https://redis.io/commands/bf.reserve/
SCHEDULER_DUPEFILTER_ERROR_RATE = 0.0001  # 错误率
SCHEDULER_DUPEFILTER_CAPACITY = 10000  # 容量
SCHEDULER_DUPEFILTER_PERSIST = True  # 过滤器持久化
