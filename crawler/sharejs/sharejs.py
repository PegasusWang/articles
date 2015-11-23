#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
import os
import requests
from extract import extract, extract_all
from tornado import gen
from async_spider import AsySpider
from pprint import pprint


def get_all_tag_urls(url='http://www.sharejs.com/codes/'):
    html = requests.get(url).content.decode('utf-8')
    tag_urls = extract_all('<a href="', '"',
                           extract('<div class="tags_cloud">', '</ul>', html))
    base_url = 'http://www.sharejs.com%s'
    tag_urls = [base_url % i for i in tag_urls]
    tag_urls = [i + '?start=0' for i in tag_urls]
    return tag_urls


class TagSpider(AsySpider):
    """拿到每个分类的所有页面"""
    def handle_html(self, url, html):
        html = html.decode('utf-8')
        start_list = extract_all('<a href="?start=', '"', html)
        if start_list:
            max_query = max((int(i) for i in start_list))
            for index in range(0, max_query, 30):
                base_url = url.rsplit('=', 1)[0] + '=' + str(index)
                self.results.append(base_url)


class TagpageSpider(AsySpider):
    """处理每个tag的单独页面，这个页面可以拿到一个文章列表"""
    def handle_html(self, url, html):
        html = html.decode('utf-8')
        url_list = extract_all('<a href="', '"',
                           extract('<div class="code_list">', '</ul>', html))
        article_list = [i for i in url_list if 'author' not in i]
        base_url = 'http://www.sharejs.com'
        article_list = [base_url+i for i in article_list]
        article_list.pop(0)
        self.results.extend(article_list)


class ArticleSpider(AsySpider):
    def handle_html(self, url, html):
        """http://www.sharejs.com/codes/javascript/9067"""
        tag = url.rsplit('/', 2)[1]
        article_id = url.rsplit('/', 2)[-1]
        filename = './sharejs_html/' + tag + '_' + article_id + '.html'

        try:
            with open(filename, 'wb') as f:
                f.write(html)
                print('saving file', filename)
        except IOError:
            if not os.path.exists('./sharejs_html'):
                os.makedirs('./sharejs_html')


def test():
    urls = ['http://www.sharejs.com/codes/javascript/?start=0']
    s = TagSpider(urls)
    s.run()
    for i in sorted(s.results):
        print(i)


def test_tag_page_spider():
    urls = ['http://www.sharejs.com/codes/javascript/?start=30']
    s = TagpageSpider(urls)
    s.run()
    for i in s.results:
        print(i)


def main():
    tag_urls = get_all_tag_urls()

    tag_spider = TagSpider(tag_urls)    # 拿到所有tag的所有页面
    tag_spider.run()

    tag_page_urls = list(set(tag_spider.results))   # 拿到所有tag页面下所有的文章
    tag_page_spider = TagpageSpider(tag_page_urls)
    tag_page_spider.run()

    article_urls = list(set(tag_page_spider.results))    # 抓取文章
    article_spider = ArticleSpider(article_urls)
    article_spider.run()


if __name__ == '__main__':
    """稍等，少年..."""
    main()
