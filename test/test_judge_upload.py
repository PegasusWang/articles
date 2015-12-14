#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
from crawler.judge_upload import exist_or_insert, is_uploaded, insert_uploaded


def test_exist_or_insert():
    assert exist_or_insert('')


def test_is_uploaded():
    title = "我是测试题20151612"
    assert not is_uploaded(title)
    insert_uploaded(title)
    assert is_uploaded(title)
