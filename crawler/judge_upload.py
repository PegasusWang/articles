#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""用来判断是不是已经上传到博客了
通过title字段判断，存储在表uploaded
"""

import _env
from lib._db import get_collection
from config.config import CONFIG


DB = CONFIG.MONGO.DATABASE
_COLL = get_collection(DB, 'uploaded')
TITLE_SET = set()
for doc in _COLL.find().batch_size(1000):
    TITLE_SET.add(doc.get('title'))


def is_uploaded(title):
    return title in TITLE_SET


def insert_uploaded(title):
    _COLL.update(
        {'title': title},
        {
            '$set': {'title': title}
        },
        True
    )


def exist_or_insert(title):
    """不存在则插入并返回Flase
    存在直接返回True"""
    if not title:    # None or '' as True
        return True
    if not is_uploaded(title):
        insert_uploaded(title)
        return False
    else:
        return True


if __name__ == '__main__':
    print DB
