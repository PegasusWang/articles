#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from extract import extract
from tornado import gen
from async_spider import AsySpider
from lib._db import get_collection
from jb51_parse import parse_jb51


class Jb51Spider(AsySpider):
    def __init__(self, urls, concurrency=10, results=None, **kwargs):
        super(Jb51Spider, self).__init__(urls, concurrency, results, **kwargs)
        self.db = get_collection('test', 'articles', 'motor')    # change coll

    @gen.coroutine
    def update(self, url, data_dict):
        yield self.db.update(
            {'source_url': url},
            {
                '$set': data_dict
            },
            True
        )

    @gen.coroutine
    def handle_html(self, url, html):
        print(url)
        data = parse_jb51(html)
        data['source_url'] = url
        yield self.update(url, data)


if __name__ == '__main__':
    urls = []
    for page in range(960, 964):
        urls.append('http://www.jb51.net/article/%s.htm' % page)
    s = Jb51Spider(urls)
    s.run()
