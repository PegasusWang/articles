#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
import pytest
from models.post import Post
from models.user import User
from tornado.ioloop import IOLoop
from tornado.testing import gen_test, AsyncTestCase
from motorengine.connection import connect
from config.config import CONFIG


save_user = {
    'name': '老王',
    'slug': 'lao-wang',
    'email': 'test@qq.com',
    'password_hash': 'testtest',
}


class TestModelUser(AsyncTestCase):
    def setUp(self):
        self.io_loop = IOLoop.current()
        connect(CONFIG.MONGO.DATABASE, host=CONFIG.MONGO.HOST,
                port=CONFIG.MONGO.PORT,
                io_loop=self.io_loop)    # connect mongoengine

    @gen_test
    def test_create(self):
        user = yield User.objects.create(**save_user)
        print(user._id)
        assert user is not None
        num = yield User.objects.filter(slug='lao-wang').delete()
        assert num == 1
