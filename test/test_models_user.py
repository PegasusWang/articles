#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
from models.user import User
from tornado import gen
from tornado.ioloop import IOLoop
from motorengine.connection import connect
from config.config import CONFIG
from uuid import uuid4


def gen_session():
    return str(uuid4())


save_user = {
    'name': 'Pegasus',
    'slug': 'pegasus',
    'email': '291374108@qq.com',
    'session': '6355be28-4a80-4a22-bd03-1550faca5487',
}


@gen.coroutine
def test_create():
    user = yield User.objects.create(**save_user)
    assert user is not None


@gen.coroutine
def test_get():
    user = yield User.objects.get('5697740b70fd902a76421987')
    print(user.name)
    assert user is not None


connect(CONFIG.MONGO.DATABASE, host=CONFIG.MONGO.HOST,
        port=CONFIG.MONGO.PORT,
        io_loop=IOLoop.current())    # motorengine connect

#IOLoop.current().run_sync(test_create)
IOLoop.current().run_sync(test_get)
