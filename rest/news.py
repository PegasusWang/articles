#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from bson.objectid import ObjectId
from bson.json_util import dumps
from rest_handler import RestHandler
from tornado import gen, escape
from tornado.web import addslash, url
from lib.format_tools import format_news_list
from pprint import pprint


class BaseNews(RestHandler):
    @property
    def _coll(self, coll_name='news'):
        return getattr(self.application._motor, coll_name)


class News(BaseNews):
    @gen.coroutine
    def get(self, news_id):
        coll = self._coll
        try:
            news = yield coll.find_one(
                {'_id': int(news_id)}
            )
            news = news or {}
        except:
            import traceback
            traceback.print_exc()
            news = {}

        if news:
            self.write_object(0, 'success', news)
        else:
            self.write_object(404, 'fail', news)


class NewsPage(BaseNews):
    @gen.coroutine
    def get(self):
        offset = int(self.get_query_argument('offset', 0))
        limit = int(self.get_query_argument('limit', 10))
        print(offset, limit)
        cursor = self._coll.find().sort([('time', -1)]).limit(limit).skip(offset)
        res = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            res.append(doc)
        escape.json_encode(res)
        self.write_batches(0, 'success', res)


urls = [
    url(r'/api/news/?', NewsPage),
    url(r'/api/news/(\w+)/?', News),
]
