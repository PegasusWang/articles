#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
import requests
from extract import extract, extract_all
from tornado import gen
from async_spider import AsySpider


def get_all_tag_urls(url='http://www.sharejs.com/codes/'):
    html = requests.get(url).content.decode('utf-8')
    tag_urls = extract_all('<a href="', '"',
                           extract('<div class="tags_cloud">', '</ul>', html))
    base_url = 'http://www.sharejs.com%s'
    tag_urls = [base_url%url for url in tag_urls]
    return tag_urls


class SharejsSpider(AsySpider):
    def handle_html(self, url, html):
        pass


if __name__ == '__main__':
    for i in get_all_tag_urls():
        print(i)
