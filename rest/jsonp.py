#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.escape import json_encode


class JsonpHandler(RequestHandler):

    def write_json(self, data_dict):
        """根据是否含有callback请求参数自动返回json或者jsonp调用"""
        callback = self.get_argument('callback', None)
        print(callback)
        if callback is not None:
            jsonp = "{jsfunc}({json});".format(jsfunc=callback,
                                               json=json_encode(data_dict))
            self.set_header('Content-Type', 'application/javascript')
            self.write(jsonp)
        else:
            self.write(data_dict)
