#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.escape import json_encode


class JsonpHandler(RequestHandler):
    def write_jsonp(self, data_dict):
        callback = self.get_argument('callback')
        jsonp = "{jsfunc}({json});".format(jsfunc=callback,
                                           json=json_encode(data_dict))
        self.set_header('Content-Type', 'application/javascript')
        self.write(jsonp)
