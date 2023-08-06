# -*- coding:utf-8 -*-
"""
@desc: 
"""
from scrapy import Spider
from . import defaults


class AttributeDict(dict):
    __slots__ = ()
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def get_queues(spider:Spider):
    pass