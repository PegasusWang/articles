#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from bson.objectid import ObjectId
from bson.json_util import dumps
from jsonp import JsonpHandler
from tornado import gen
from tornado.web import addslash, url


class BaseHandler(JsonpHandler):
    def initialize(self, coll):
        self.coll = getattr(self.application._motor, coll)


class Post(BaseHandler):
    """通过id返回文章json数据"""
    @gen.coroutine
    def get(self, post_id):
        try:
            article = yield self.coll.find_one(
                {'_id': ObjectId(post_id)}
            )
            article = article or {}
            if article:
                yield self.coll.update(
                    {'_id': ObjectId(post_id)},
                    {
                        '$inc': {'read_count': 1}
                    },
                    True
                )
        except:
            article = {}

        self.write_json(dumps(article))   # or del article["_id"]


class UpdatePost(JsonpHandler):
    """更新文章信息"""
    pass


articles_url = [
    url(r'/post/(\w+)/?', Post, dict(coll='Articles'))
]
