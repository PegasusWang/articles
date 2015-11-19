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
        self.db = get_collection('test', 'Articles', 'motor')

    @gen.coroutine
    def update(self, url, data_dict):
        yield self.db.update(
            {'source_url': url},
            {
                '$set': data_dict
            },
            True
        )

    def handle_html(self, url, html):
        html = extract('<div class="dxy_main">',
                       '<div class="art_bot_ad">', html)
        html = html.decode('gb18030')
        data = parse_jb51(html)
        data['source_url'] = url
        self.update(url, data)
        print(data)


if __name__ == '__main__':
    urls = []
    for page in range(8, 10):
        urls.append('http://www.jb51.net/article/%s.htm' % page)
    s = Jb51Spider(urls)
    s.run()
