#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handlers import (
    base,
)
from rest import (
    articles,
)
from tornado.web import url

url_patterns = []
url_patterns.extend(articles.articles_url)
url_patterns.append(url(r'.*', base.PageNotFoundHandler))    # catch return 404
