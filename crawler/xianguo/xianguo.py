#!/usr/bin/env python
# -*- coding:utf-8 -*-


import _env
import json
import requests
from pprint import pprint
from lib._db import get_collection
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

URL = 'http://api.xianguo.com/i/status/get.json?key=36d979af3f6cecd87b89720d3284d420'


def to_dict(form):
    d = {}
    arg_list = form.rstrip('&').split('&')
    for i in arg_list:
        k = i.split('=')[0]
        v = i.split('=')[1]
        d[k] = v
    return d


def fetch(url, data_dict=None):
    return requests.post(url, data=data_dict).text

_COLL = get_collection('test', 'news')


def xianguo_spider(q, max_news_num=1000):
    while True:
        while not q.empty():
            url, data_dict = q.get()
            html = fetch(url, data_dict)

            if not html or html == 'null':    # xianguo may returns null
                return

            o = json.loads(html)
            to_save = ['docid', 'source', 'content',
                       'url', 'title', 'time', 'brief']
            id_list = []

            for i in o:
                d = {}
                docid = i.get('id')
                id_list.append(docid)
                section_id = i.get('user').get('id')
                source = i.get('user').get('username')
                content = i.get('linkcontent').get('content')
                url = i.get('linkcontent').get('originalurl')
                title = i.get('linkcontent').get('title')
                time = i.get('time')
                if time is None or time == 'None':
                    time = 0

                brief = i.get('content')
                for k, v in list(locals().items()):
                    if k in to_save:
                        d[k] = v

                _COLL.update(
                    {'_id': int(docid)},
                    {
                        '$set': d
                    },
                    True
                )
            maxid = min(id_list)

            form_dict = dict(
                devicemodel='motorola-XT1079',
                isShowContent=1,
                maxid=int(maxid),
                sectionid=int(section_id),
                sectiontype=0,
                version=77,
                count=25,
                udid=355456060447393,
                devicetype=5,
                isThumb=0
            )
            print('new url', form_dict.get('maxid'), form_dict.get('sectionid'))

            for i in id_list:
                if _COLL.find_one({'_id': int(i)}):
                    print('************Finish#############')
                    return

            q.put((URL, form_dict))    # put a tuple


all_id = """FT中文网 1185664
商业价值 1057830
智客 1967473
虎嗅网 1289851
钛媒体 1410319
创业邦 1057591
知乎每日精选 1199167
36氪 1057676
快鲤鱼 1382170
创业家 1132786
TechCrunch 中国 1847011
小众软件 1000542
极客公园 1250579
小道消息 by Fenng 1886952
爱范儿 1000806
i黑马 1236199
新智派 2271997
PingWest品玩 1379576
瘾科技 1000192
InfoQ中文站 1000521
互联网的那点事 1057660
TECH2IPO创见 1059587"""


def get_sectionid_list():
    name_list = (all_id.split('\n'))
    res = []
    for i in name_list:
        l = i.split()
        res.append(l[len(l)-1])
    return res


def main():
    q = Queue()
    formstr = 'devicemodel=motorola-XT1079&isShowContent=1&maxid=1000000000&sectionid=%d&sectiontype=0&version=77&count=25&udid=355456060447393&devicetype=5&isThumb=1&'
    for sid in get_sectionid_list():
        s = formstr % (int(sid))
        print(s)
        q.put((URL, to_dict(s)))
        xianguo_spider(q)


if __name__ == '__main__':
    main()
