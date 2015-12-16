#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""ping脚本，有新文章发布的时候通知搜索引擎. py2"""


import re
import time
import urllib2
import xmlrpclib    # py2


def ping(ping_url, site_name, site_host, post_url, rss_url):
    print('ping...', ping_url, post_url)
    rpc_server = xmlrpclib.ServerProxy(ping_url)
    result = rpc_server.weblogUpdates.extendedPing(
        site_name, site_host, "http://"+post_url, "http://"+rss_url
    )
    print(result)
    with open('ping.url', 'a+') as f:
        f.write(post_url+'\n')


def ping_all(*args, **kwds):
    ping_url_list = [
        'http://ping.baidu.com/ping/RPC2', # http://zhanzhang.baidu.com/tools/ping
        #'http://rpc.pingomatic.com/',    # must every 5 minutes
        #'http://blogsearch.google.com/ping/RPC2',
        #'http://api.my.yahoo.com/RPC2',
        #'http://blog.youdao.com/ping/RPC2',
        #'http://ping.feedburner.com',
    ]
    for url in ping_url_list:
        try:
            ping(url, *args, **kwds)
        except Exception:
            print('ping fail', post_url)
            continue


def get_all_post_url(rss_url='http://jishushare.com/sitemap-posts.xml'):
    """rss_url 博客的rss地址"""
    response = urllib2.urlopen(rss_url)
    html = response.read()
    pat = re.compile('<loc>http://(.*?)</loc>')
    url_list = ['http://'+url for url in pat.findall(html)]
    return set(url_list)


def get_already_ping_url(f='./ping.url'):
    with open(f, 'r+') as f:
        return set([url.strip() for url in f.readlines() if url])


def test():
    site_name = "技术分享网"
    site_host = "http://jishushare.com/"
    post_url = 'http://jishushare.com/duo-xian-cheng-yi-bu-yi-bu-duo-jin-cheng-pa-chong/'
    rss_url = "http://jishushare.com/sitemap-posts.xml"
    ping_all(site_name, site_host, post_url, rss_url)


def ping_jishushare():
    to_ping_url_list = get_all_post_url() - get_already_ping_url()
    site_name = "技术分享网"
    site_host = "http://jishushare.com/"
    rss_url = "http://jishushare.com/sitemap-posts.xml"
    for post_url in to_ping_url_list:
        time.sleep(10)
        ping_all(site_name, site_host, post_url, rss_url)


def ping_jishushare():
    rss_url = 'http://ningning.today/sitemap.xml'
    to_ping_url_list = get_all_post_url(rss_url) - get_already_ping_url()
    site_name = "Pegasus的博客"
    site_host = "http://ningning.today/"
    for post_url in to_ping_url_list:
        time.sleep(10)
        ping_all(site_name, site_host, post_url, rss_url)


if __name__ == '__main__':
    ping_jishushare()
