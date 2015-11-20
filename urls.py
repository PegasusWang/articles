#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handlers import (
    base,
)
from rest import (
    articles,
)
from tornado.web import url
from lib._db import get_collection


url_patterns = [
    url(r'/post/(\w+)/?', articles.ArticlesHandler,
        dict(coll=get_collection('test', 'Articles', 'motor'))),

    url(r'.*', base.PageNotFoundHandler),    # catch return 404 page
]
