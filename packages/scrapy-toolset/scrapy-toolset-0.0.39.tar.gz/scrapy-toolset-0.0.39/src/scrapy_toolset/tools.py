# -*- coding:utf-8 -*-
"""
@desc: 
"""
import json
import re
import six

import traceback
from pprint import pformat
import datetime
from pymongo import ReplaceOne, UpdateOne

_regexs = {}

def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s

def str_to_bytes(s, encoding='utf-8'):
    if six.PY3 and isinstance(s, str):
        return s.encode(encoding)
    return s


def replace_str(source_str, regex, replace_str=""):
    """
    @summary: 替换字符串
    ---------
    @param source_str: 原字符串
    @param regex: 正则
    @param replace_str: 用什么来替换 默认为''
    ---------
    @result: 返回替换后的字符串
    """
    str_info = re.compile(regex)
    return str_info.sub(replace_str, source_str)


def get_info(html, regexs, allow_repeat=True, fetch_one=False, split=None):
    regexs = isinstance(regexs, str) and [regexs] or regexs

    infos = []
    for regex in regexs:
        if regex == "":
            continue

        if regex not in _regexs.keys():
            _regexs[regex] = re.compile(regex, re.S)

        if fetch_one:
            infos = _regexs[regex].search(html)
            if infos:
                infos = infos.groups()
            else:
                continue
        else:
            infos = _regexs[regex].findall(str(html))

        if len(infos) > 0:
            # print(regex)
            break

    if fetch_one:
        infos = infos if infos else ("",)
        return infos if len(infos) > 1 else infos[0]
    else:
        infos = allow_repeat and infos or sorted(set(infos), key=infos.index)
        infos = split.join(infos) if split else infos
        return infos


def table_json(table, save_one_blank=True):
    """
    将表格转为json 适应于 key：value 在一行类的表格
    @param table: 使用selector封装后的具有xpath的selector
    @param save_one_blank: 保留一个空白符
    @return:
    """
    data = {}

    trs = table.xpath(".//tr")
    for tr in trs:
        tds = tr.xpath("./td|./th")

        for i in range(0, len(tds), 2):
            if i + 1 > len(tds) - 1:
                break

            key = tds[i].xpath("string(.)").extract_first(default="").strip()
            value = tds[i + 1].xpath("string(.)").extract_first(default="").strip()
            value = replace_str(value, "[\f\n\r\t\v]", "")
            value = replace_str(value, " +", " " if save_one_blank else "")

            if key:
                data[key] = value

    return data


def get_table_row_data(table):
    """
    获取表格里每一行数据
    @param table: 使用selector封装后的具有xpath的selector
    @return: [[],[]..]
    """

    datas = []
    rows = table.xpath(".//tr")
    for row in rows:
        cols = row.xpath("./td|./th")
        row_datas = []
        for col in cols:
            data = col.xpath("string(.)").extract_first(default="").strip()
            row_datas.append(data)
        datas.append(row_datas)

    return datas


def rows2json(rows, keys=None):
    """
    将行数据转为json
    @param rows: 每一行的数据
    @param keys: json的key，空时将rows的第一行作为key
    @return:
    """
    data_start_pos = 0 if keys else 1
    datas = []
    keys = keys or rows[0]
    for values in rows[data_start_pos:]:
        datas.append(dict(zip(keys, values)))

    return datas


def get_form_data(form):
    """
    提取form中提交的数据
    :param form: 使用selector封装后的具有xpath的selector
    :return:
    """
    data = {}
    inputs = form.xpath(".//input")
    for input in inputs:
        name = input.xpath("./@name").extract_first()
        value = input.xpath("./@value").extract_first()
        if name:
            data[name] = value

    return data


def get_json(json_str):
    """
    @summary: 取json对象
    ---------
    @param json_str: json格式的字符串
    ---------
    @result: 返回json对象
    """

    try:
        return json.loads(json_str) if json_str else {}
    except Exception as e1:
        try:
            json_str = json_str.strip()
            json_str = json_str.replace("'", '"')
            keys = get_info(json_str, "(\w+):")
            for key in keys:
                json_str = json_str.replace(key, '"%s"' % key)

            return json.loads(json_str) if json_str else {}

        except Exception as e2:
            traceback.print_exc()

        return {}


def jsonp2json(jsonp):
    """
    将jsonp转为json
    @param jsonp: jQuery172013600082560040794_1553230569815({})
    @return:
    """
    try:
        return json.loads(re.match(".*?({.*}).*", jsonp, re.S).group(1))
    except:
        raise ValueError("Invalid Input")


def dumps_json(json_, indent=4, sort_keys=False):
    """
    @summary: 格式化json 用于打印
    ---------
    @param json_: json格式的字符串或json对象
    ---------
    @result: 格式化后的字符串
    """
    try:
        if isinstance(json_, str):
            json_ = get_json(json_)

        json_ = json.dumps(
            json_, ensure_ascii=False, indent=indent, skipkeys=True, sort_keys=sort_keys
        )

    except Exception as e:
        json_ = pformat(json_)

    return json_


def get_json_value(json_object, key):
    """
    @summary:
    ---------
    @param json_object: json对象或json格式的字符串
    @param key: 建值 如果在多个层级目录下 可写 key1.key2  如{'key1':{'key2':3}}
    ---------
    @result: 返回对应的值，如果没有，返回''
    """
    current_key = ""
    value = ""
    try:
        json_object = (
                isinstance(json_object, str) and get_json(json_object) or json_object
        )

        current_key = key.split(".")[0]
        value = json_object[current_key]

        key = key[key.find(".") + 1:]
    except Exception as e:
        return value

    if key == current_key:
        return value
    else:
        return get_json_value(value, key)


def get_all_keys(datas, depth=None, current_depth=0):
    """
    @summary: 获取json李所有的key
    ---------
    @param datas: dict / list
    @param depth: 字典key的层级 默认不限制层级 层级从1开始
    @param current_depth: 字典key的当前层级 不用传参
    ---------
    @result: 返回json所有的key
    """

    keys = []
    if depth and current_depth >= depth:
        return keys

    if isinstance(datas, list):
        for data in datas:
            keys.extend(get_all_keys(data, depth, current_depth=current_depth + 1))
    elif isinstance(datas, dict):
        for key, value in datas.items():
            keys.append(key)
            if isinstance(value, dict):
                keys.extend(get_all_keys(value, depth, current_depth=current_depth + 1))

    return keys


def to_chinese(unicode_str):
    format_str = json.loads('{"chinese":"%s"}' % unicode_str)
    return format_str["chinese"]


def format_sql_value(value):
    if isinstance(value, str):
        value = value.strip()

    elif isinstance(value, (list, dict)):
        value = dumps_json(value, indent=None)

    elif isinstance(value, (datetime.date, datetime.time)):
        value = str(value)

    elif isinstance(value, bool):
        value = int(value)

    return value


def list2str(datas):
    """
    列表转字符串
    :param datas: [1, 2]
    :return: (1, 2)
    """
    data_str = str(tuple(datas))
    data_str = re.sub(",\)$", ")", data_str)
    return data_str


def make_insert_sql(
        table, data, auto_update=False, update_columns=(), insert_ignore=False
):
    """
    @summary: 适用于mysql， oracle数据库时间需要to_date 处理（TODO）
    ---------
    @param table:
    @param data: 表数据 json格式
    @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
    @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
    @param insert_ignore: 数据存在忽略
    ---------
    @result:
    """

    keys = ["`{}`".format(key) for key in data.keys()]
    keys = list2str(keys).replace("'", "")

    values = [format_sql_value(value) for value in data.values()]
    values = list2str(values)

    if update_columns:
        if not isinstance(update_columns, (tuple, list)):
            update_columns = [update_columns]
        update_columns_ = ", ".join(
            ["{key}=values({key})".format(key=key) for key in update_columns]
        )
        sql = (
                "insert%s into `{table}` {keys} values {values} on duplicate key update %s"
                % (" ignore" if insert_ignore else "", update_columns_)
        )

    elif auto_update:
        sql = "replace into `{table}` {keys} values {values}"
    else:
        sql = "insert%s into `{table}` {keys} values {values}" % (
            " ignore" if insert_ignore else ""
        )
    sql = sql.format(table=table, keys=keys, values=values).replace("None", "null")
    return sql


def make_update_sql(table, data, condition):
    """
    @summary: 适用于mysql， oracle数据库时间需要to_date 处理（TODO）
    ---------
    @param table:
    @param data: 表数据 json格式
    @param condition: where 条件
    ---------
    @result:
    """
    key_values = []

    for key, value in data.items():
        value = format_sql_value(value)
        if isinstance(value, str):
            key_values.append("`{}`={}".format(key, repr(value)))
        elif value is None:
            key_values.append("`{}`={}".format(key, "null"))
        else:
            key_values.append("`{}`={}".format(key, value))

    key_values = ", ".join(key_values)

    sql = "update `{table}` set {key_values} where {condition}"
    sql = sql.format(table=table, key_values=key_values, condition=condition)
    return sql


def make_batch_sql(
        table, datas, auto_update=False, update_columns=(), update_columns_value=()
):
    """
    @summary: 生产批量的sql
    ---------
    @param table:
    @param datas: 表数据 [{...}]
    @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
    @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
    @param update_columns_value: 需要更新的列的值 默认为datas里边对应的值, 注意 如果值为字符串类型 需要主动加单引号， 如 update_columns_value=("'test'",)
    ---------
    @result:
    """
    if not datas:
        return

    keys = list(datas[0].keys())
    values_placeholder = ["%s"] * len(keys)

    values = []
    for data in datas:
        value = []
        for key in keys:
            current_data = data.get(key)
            current_data = format_sql_value(current_data)

            value.append(current_data)

        values.append(value)

    keys = ["`{}`".format(key) for key in keys]
    keys = list2str(keys).replace("'", "")

    values_placeholder = list2str(values_placeholder).replace("'", "")

    if update_columns:
        if not isinstance(update_columns, (tuple, list)):
            update_columns = [update_columns]
        if update_columns_value:
            update_columns_ = ", ".join(
                [
                    "`{key}`={value}".format(key=key, value=value)
                    for key, value in zip(update_columns, update_columns_value)
                ]
            )
        else:
            update_columns_ = ", ".join(
                ["`{key}`=values(`{key}`)".format(key=key) for key in update_columns]
            )
        sql = "insert into `{table}` {keys} values {values_placeholder} on duplicate key update {update_columns}".format(
            table=table,
            keys=keys,
            values_placeholder=values_placeholder,
            update_columns=update_columns_,
        )
    elif auto_update:
        sql = "replace into `{table}` {keys} values {values_placeholder}".format(
            table=table, keys=keys, values_placeholder=values_placeholder
        )
    else:
        sql = "insert ignore into `{table}` {keys} values {values_placeholder}".format(
            table=table, keys=keys, values_placeholder=values_placeholder
        )

    return sql, values


def make_actions(index, doc_type, datas, auto_update, id_column=None, params={}, update_columns=()):
    for data in datas:
        action = {}
        action['_index'] = index
        action['_type'] = doc_type
        if auto_update:
            action['_op_type'] = 'index'
            action['_source'] = data
        else:
            action['_op_type'] = 'update'
            action['source'] = {
                'upsert': data,
                'doc': {column: data[column] for column in update_columns}
            }
        if id_column:
            action['_id'] = data[id_column]
        action.update(params)
        yield action


def make_mongo_action(data, id=None, filter_columns=(), update_columns=(), auto_update=False, **kwargs):
    id = id or data.get("_id")
    if id:
        filter = {"_id": id}
    else:
        if not filter_columns:
            raise ValueError('mongodbItem未配置id或筛选条件, 请为Item设置`_id`字段或 设置filter_columns')
        else:
            filter = {column: data[column] for column in filter_columns}
    if auto_update:
        # 覆盖写入
        action = ReplaceOne(filter, data, upsert=True)
    else:
        if update_columns:
            # 更新字段
            action = UpdateOne(filter, {"$set": {column: data[column] for column in update_columns}}, upsert=True)
        else:
            # 未配置要更新的字段，则进行  有则略过，无则插入
            action = UpdateOne(filter, {'$setOnInsert': data}, upsert=True)
    return action


def make_mongo_batch_action(datas, filter_columns=(), update_columns=(), auto_update=False, **kwargs):
    return [make_mongo_action(data=data, **data, filter_columns=filter_columns, auto_update=auto_update,
                              update_columns=update_columns) for data in datas]
