#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from bson.objectid import ObjectId
from bson.json_util import dumps
from jsonp import JsonpHandler
from tornado import gen
from tornado.web import addslash, url
from lib.format_list import format_news_list


class BaseNews(JsonpHandler):
    @property
    def _coll(self, coll_name='news'):
        return getattr(self.application._motor, coll_name)


class News(BaseNews):

    @gen.coroutine
    def get(self, news_id):
        coll = self._coll
        try:
            news = yield coll.find_one(
                {'_id': ObjectId(news_id)}
            )
            news = news or {}
        except:
            news = {}

        self.write_json(dumps(news))   # or del article["_id"]


class NewsPage(BaseNews):
    @gen.coroutine
    def get(self):
        offset = int(self.get_query_argument('offset', 0))
        limit = self.get_query_arguments('limit', 10)


articles_url = [
    url(r'/post/(\w+)/(\w+)/?', News),
]
