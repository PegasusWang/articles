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
        try:
            self.write_json(dumps(article))   # or del article["_id"]
        except:
            self.write_json(dumps({}))
