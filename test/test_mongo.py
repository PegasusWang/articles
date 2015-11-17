#!/usr/bin/env python
# -*- coding: utf-8 -*-


import _env
from lib._db import get_collection
from bson.objectid import ObjectId
from pprint import pprint


def test():
    coll = get_collection('test', 'Articles')
    doc = coll.find_one({'_id': ObjectId('5649e9edea282e17fa5511f7')})
    print(type(doc))
    pprint(doc)


if __name__ == '__main__':
    test()
