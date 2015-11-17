#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib import _db
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.options import options

from settings import settings
from urls import url_patterns


class ArticlesApp(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)
        self._redis = _db.redis_client
        self._motor = _db.motor_client


def main():
    app = ArticlesApp()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
