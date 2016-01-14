#!/usr/bin/env python
# -*- coding:utf-8 -*-

from uuid import uuid4


def gen_uuid_32():
    return str(uuid4()).replace('-', '')


# pip install M2Crypto
# http://stackoverflow.com/questions/817882/unique-session-id-in-python/6092448#6092448

def gen_session():
    return str(uuid4())
