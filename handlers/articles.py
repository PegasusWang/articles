#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from tornado import gen
from tornado.web import RequestHandler, HTTPError, addslash
from bson.objectid import ObjectId
from bson.json_util import dumps


class ArticlesHandler(RequestHandler):
    def initialize(self, coll):
        self.coll = coll

    @addslash
    @gen.coroutine
    def get(self, post_id):
        print(post_id, type(post_id))
        article = yield self.coll.find_one(
            {'_id': ObjectId(post_id)}
        )
        print(type(article))
        if article:
            self.write(dumps(article))    # or del article["_id"]
        else:
            self.write({})
