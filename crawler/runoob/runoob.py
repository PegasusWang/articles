#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import os
import urlparse
import traceback
import requests
from async_spider import AsySpider
from extract import extract, extract_all


def get_sub_urls(url):
    """从主页拿到所有的子分类"""
    html = requests.get(url).content
    sub = extract_all('<a class="item-top item-1" href="',
                      '"', html)
    return sub


class TagSpider(AsySpider):
    """进入分类后左边有一列是这个分类的所有文章，这个handle_html就是拿到所有
    这些文章的url, 你可以先输出到一个文件，供SubtagSpider读取。
    """
    def handle_html(self, url, html):
        html = html.decode('utf-8')    # 先decode下，参数参考html的charset
        left_column_tag = extract('id="leftcolumn"', '</div>',
                                  html)
        urls = extract_all('href="', '"', left_column_tag)
        base_url = 'http://www.runoob.com'

        # 这句是把相对路径/path/html-tutorial
        # 变成http://www.runoob.com/path/html-tutorial
        urls = [urlparse.urljoin(base_url, url)
                for url in urls if base_url not in url]

        # 保存所有url供SubtagSpider读取
        with open('urls.txt', 'a+') as f:
            for i in urls:
                f.write(i+'\n')


class SubtagSpider(AsySpider):
    """这个处理上一步得到的所有url，因为暂时不用处理，可以类似下边这样保存。
    """
    def handle_html(self, url, html):
        url_scheme = urlparse.urlparse(url)
        path = url_scheme.path

        # 用url的有意义的一部分命名文件
        # http://www.runoob.com/html/html-tutorial.html得到的
        # filename为html_html-tutorial.html
        # 注意这个保存到当前文件夹，别把html加入版本库，移出去保存

        try:
            filename = './runoob_html/' + path.strip('/').replace('/', '_')
            with open(filename, 'wb') as f:
                f.write(html)
            print('saving file...^_^', filename)

        except IOError:    # 当前文件没有runoob_html文件夹
            if not os.path.exists('./runoob_html'):
                os.makedirs('./runoob_html')


def test_get_sub_urls():
    url = 'http://www.runoob.com'
    for i in get_sub_urls(url):
        print i


def test_tag_spider():
    urls = ['http://www.runoob.com/html/html-tutorial.html']
    s = TagSpider(urls)
    s.run()


def test_sub_spider():
    urls = ['http://www.runoob.com/html/html-editors.html']
    s = SubtagSpider(urls)
    s.run()


def main():
    # 三步走
    url = 'http://www.runoob.com'
    tag_urls = get_sub_urls(url)    # 所有分类

    # 所有分类页面的主页面左边一列有这个分类下的所有url，下边输出到urls.txt里边
    # 可以参考TagSpider的handle_html
    tag_spider = TagSpider(tag_urls)
    tag_spider.run()

    # 读取上边保存的urls.txt
    with open('urls.txt', 'r') as f:
        urls = [i.strip() for i in f.readlines() if i]
    urls = list(set(urls))    # remove duplicate
    s = SubtagSpider(urls)
    s.run()


if __name__ == '__main__':
    #test_get_sub_urls()
    #test_tag_spider()
    #test_sub_spider()
    main()
