#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
import json
import time
from lib._db import get_collection


def cur_timestamp():
    return int(time.time() * 1000)


def replace_post(post_data):
    d = {
        "id": 5,
        "title":        "my blog post title",
        "slug":         "my-blog-post-title",
        "markdown":     "the *markdown* formatted post body",
        "html":         "the <i>html</i> formatted post body",
        "image":        null,
        "featured":     0,
        "page":         0,
        "status":       "published",
        "language":     "en_US",
        "meta_title":   null,
        "meta_description":null,
        "author_id":    1, // the first user created has an id of 1
        "created_at":   1283780649000, // epoch time in millis
        "created_by":   1, // the first user created has an id of 1
        "updated_at":   1286958624000, // epoch time in millis
        "updated_by":   1, // the first user created has an id of 1
        "published_at": 1283780649000, // epoch time in millis
        "published_by": 1 // the first user created has an id of 1
    }

def migrate():
    res = {
        "meta": {
            "exported_on": cur_timestamp(),
            "version": "003"
        }
    }


def get_posts():
    coll = get_collection('test', 'articles')

    for doc in coll.find().batch_size(1000):




if __name__ == '__main__':
    main()
