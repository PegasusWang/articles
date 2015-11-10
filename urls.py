#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handlers import (
    base, admin,
)
from tornado.web import url


url_patterns = [
    # leancloud api
    url(r'/api/data.json', leancloud_handler.LeanClassHandler),

    url(r'/?', site.SiteHandler, dict(class_name='Girls')),
    url(r'/show/([\w_]+)/?', show.ShowHandler),

    url(r'.*', base.PageNotFoundHandler),    # catch return 404 page
]
