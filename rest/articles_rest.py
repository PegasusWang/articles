#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import traceback
from bson.objectid import ObjectId
from rest_handler import RestHandler
from tornado import gen
from tornado.web import url


class Post(RestHandler):
    """通过collection名字和id返回文章json数据"""
    @gen.coroutine
    def get(self, coll_name, post_id):
        coll = getattr(self.application._motor, coll_name)
        print(coll_name, post_id)
        try:
            article = yield coll.find_one(
                {'_id': ObjectId(post_id)}
            )
            article = article if article else {}
            if article:
                yield coll.update(
                    {'_id': ObjectId(post_id)},
                    {
                        '$inc': {'read_count': 1}
                    },
                    True
                )
        except Exception:
            traceback.print_exc()
            article = {}

        if article:
            self.write_object(0, 'success', article)
        else:
            self.write_object(404, 'fail', article)

    @gen.coroutine
    def delete(self, post_id):
        pass


class PostPage(RestHandler):
    @gen.coroutine
    def get(self):
        pass


URL_ROUTES = [
    url(r'/api/post/(\w+)/(\w+)/?', Post),
]
