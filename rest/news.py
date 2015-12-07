#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from bson.objectid import ObjectId
from bson.json_util import dumps
from jsonp import JsonpHandler
from tornado import gen
from tornado.web import addslash, url


class Post(JsonpHandler):
    """通过collection名字和id返回文章json数据"""
    @gen.coroutine
    def get(self, coll_name, post_id):
        coll = getattr(self.application._motor, coll_name)
        try:
            article = yield coll.find_one(
                {'_id': ObjectId(post_id)}
            )
            article = article or {}
            if article:
                yield coll.update(
                    {'_id': ObjectId(post_id)},
                    {
                        '$inc': {'read_count': 1}
                    },
                    True
                )
        except:
            article = {}

        self.write_json(dumps(article))   # or del article["_id"]

    @gen.coroutine
    def delete(self, post_id):
        pass


articles_url = [
    url(r'/post/(\w+)/(\w+)/?', Post),
]
