#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""代码片段相关接口"""

import _env
import traceback
from rest_handler import RestHandler
from tornado import gen
from tornado.web import url


class BaseCodes(RestHandler):
    @property
    def _coll(self, coll_name='codes'):
        return getattr(self.application._motor, coll_name)


class Codes(BaseCodes):
    @gen.coroutine
    def get(self, code_id):
        coll = self._coll
        try:
            news = yield coll.find_one({'_id': int(code_id)})
            news = news or {}
        except Exception:
            traceback.print_exc()
            news = {}

        if news:
            self.write_object(0, 'success', news)
        else:
            self.write_object(404, 'fail', news)


class CodesKindPage(BaseCodes):
    @gen.coroutine
    def get(self):
        res = []
        try:
            offset = int(self.get_query_argument('offset', 0))
            limit = int(self.get_query_argument('limit', 10))
            kind = self.get_argument('kind', None)
            if offset < 0 or limit > 50:
                offset, limit = 0, 10

            cursor = self._coll.find({'kind': kind})
            cursor.skip(offset).limit(limit)

            while (yield cursor.fetch_next):
                doc = cursor.next_object()
                res.append(doc)

        except Exception:
            traceback.print_exc()
            self.write_batches(404, 'fail', [])
            return

        self.write_batches(0, 'success', res)


URL_ROUTES = [
    url(r'/api/codes/?', CodesKindPage),
    url(r'/api/codes/(\w+)/?', Codes),
]
