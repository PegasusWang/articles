#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
import json
import time
from lib._db import get_collection


def cur_timestamp():
    return int(time.time() * 1000)

users = [
    {
        "id":           1,
        "name":         "man",
        "slug":         "man",
        "email":        "user@example.com",
        "image":        None,
        "cover":        None,
        "bio":          None,
        "website":      None,
        "location":     None,
        "accessibility": None,
        "status":       "active",
        "language":     "zh_CN",
        "meta_title":   None,
        "meta_description": None,
        "last_login":   None,
        "created_at":   1283780649000,
        "created_by":   1,
        "updated_at":   1286958624000,
        "updated_by":   1
    }
]

def replace_post(post_data):
    d = {
        "id": 5,
        "title":        "my blog post title",
        "slug":         "my-blog-post-title",
        "markdown":     "the *markdown* formatted post body",
        #"html":         "the <i>html</i> formatted post body",
        "image":        None,
        "featured":     0,
        "page":         0,
        "status":       "published",
        "language":     "zh_CN",
        "meta_title":   None,
        "meta_description": None,
        "author_id":    1,
        "created_at":   cur_timestamp(),
        "created_by":   1,
        "updated_at":   cur_timestamp(),
        "updated_by":   1,
        "published_at": cur_timestamp(),
        "published_by": 1
    }
    d['id'] = int(post_data['source_url'].rsplit('/', 1)[1].split('.')[0])
    d['title'] = post_data['title']
    d['slug'] = post_data['title'].replace(' ', '-').lower()
    d['markdown'] = post_data['content']
    return d


def migrate():
    res = {
        "meta": {
            "exported_on": cur_timestamp(),
            "version": "003"
        }
    }
    coll = get_collection('test', 'articles')

    posts = []
    tags = []
    posts_tags = []
    tag_id = 0

    #for doc in coll.find().batch_size(1000):
    doc = coll.find_one()
    if doc:
        posts.append(replace_post(doc))
        post_id = int(doc['source_url'].rsplit('/', 1)[1].split('.')[0])
        tag_list = doc.get('tag_list')
        tag = tag_list[0] if tag_list else ''
        if tag:
            tag_id += 1
            tags.append({
                "id": tag_id,
                "name": tag,
                "slug": tag.replace(' ', '-'),
                "description": ""
            })
            posts_tags.append({"tag_id": tag_id, "post_id": post_id})

    data = {
        "posts": posts,
        "tags": tags,
        "posts_tags": posts_tags,
        "users": users
    }
    res["data"] = data
    return res


if __name__ == '__main__':
    print(migrate())
