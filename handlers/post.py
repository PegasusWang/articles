#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .base import BaseHandler
from tornado.gen import coroutine
from models.post import Post


class PostHandler(BaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user_id')

    def get(self, slug):
        pass

    def post(self):
        self.get_body_argument("title")
