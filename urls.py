#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handlers import (
    base,
)
from rest import (
    articles, news
)
from tornado.web import url

# collect all url routes from rest module
url_patterns = []
for module in [articles, news]:
    url_patterns.extend(getattr(module, 'URL_ROUTES'))

url_patterns.append(url(r'.*', base.PageNotFoundHandler))    # catch return 404
