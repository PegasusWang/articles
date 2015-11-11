#!/usr/bin/env python
# -*- coding: utf-8 -*-

from async_spider import AsySpider


class Jb51Spider(AsySpider):

    def handle_html(self, url, html):
        print(url)
        '''
        filename = url.rsplit('/', 1)[1]
        with open(filename, 'w+') as f:
            f.write(html)
        '''


if __name__ == '__main__':
    urls = []
    for page in range(1, 73000):
        urls.append('http://www.jb51.net/article/%s.htm' % page)
    s = Jb51Spider(urls)
    s.run()
