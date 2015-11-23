#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from bson.objectid import ObjectId
from bson.json_util import dumps
from jsonp import JsonpHandler
from tornado import gen
from tornado.web import RequestHandler, HTTPError, addslash


class ArticlesHandler(JsonpHandler):
    def initialize(self, coll):
        self.coll = coll

    @addslash
    @gen.coroutine
    def get(self, post_id):
        print(post_id, type(post_id))
        article = yield self.coll.find_one(
            {'_id': ObjectId(post_id)}
        )

        call = 'write_jsonp' if self.get_argument('callback', None) else 'write'
        method = getattr(self, call)

        if article:
            method(dumps(article))    # or del article["_id"]
        else:
            method({})
