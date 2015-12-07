#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from bson.objectid import ObjectId
from bson.json_util import dumps
from jsonp import JsonpHandler
from tornado import gen
from tornado.web import addslash, url
from pprint import pprint


class BasePost(JsonpHandler):
    def write_result(self, code, message, data, error=None):
        """code, message not empty"""
        res = {}
        res['code'] = code
        res['message'] = message
        if data:
            data['id'] = str(data['_id'])
            del data['_id']
            res['data'] = data
        self.write_json(res)


class Post(BasePost):
    """通过collection名字和id返回文章json数据"""
    @gen.coroutine
    def get(self, coll_name, post_id):
        coll = getattr(self.application._motor, coll_name)
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
        except:
            article = {}

        pprint(article)
        if article:
            self.write_result(0, 'success', article)
        else:
            self.write_result(404, 'fail', article)


    @gen.coroutine
    def delete(self, post_id):
        pass


articles_url = [
    url(r'/api/post/(\w+)/(\w+)/?', Post),
]
