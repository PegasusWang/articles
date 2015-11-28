#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from bson.objectid import ObjectId
from bson.json_util import dumps
from jsonp import JsonpHandler
from tornado import gen
from tornado.web import addslash, url


class ArticlesHandler(JsonpHandler):
    def initialize(self, coll):
        self.coll = getattr(self.application._motor, coll)

    @addslash
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


articles_url = [
    url(r'/post/(\w+)/?', ArticlesHandler, dict(coll='Articles'))
]
