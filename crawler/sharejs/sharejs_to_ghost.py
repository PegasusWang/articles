#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
import json
import re
import time
from lib._db import get_collection

pat = re.compile('[-#\w]+')


def find_first_tag(s):
    m = pat.search(s)
    return m.group() if m else s


def remove_china_char(s):
    if not s:
        return s
    return re.sub(ur"[\u4e00-\u9fa5]+", '', s)


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


tags = [
    {
        "id": 1000,
        "name": u'代码',
        "slug": u'代码',
        "description": ""
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
    d['title'] = post_data['title'].strip()
    d['slug'] = post_data['title'].strip().replace(' ', '-').lower()
    d['markdown'] = post_data['content'].strip()
    return d


def migrate(limit=10):
    res = {
        "meta": {
            "exported_on": cur_timestamp(),
            "version": "003"
        }
    }
    coll = get_collection('test', 'code')

    posts = []
    posts_tags = []
    index = 0

    for doc in coll.find().batch_size(1000):
        #print(doc.get('title'))
        doc_id = doc.get('_id')
        post_id = int(doc['source_url'].rsplit('/', 1)[1].split('.')[0])
        index += 1
        if index > limit:
            break

        posts.append(replace_post(doc))
        posts_tags.append(
            {"tag_id": 1000, "post_id": post_id}
        )

    data = {
        "posts": posts,
        "tags": tags,
        "posts_tags": posts_tags,
        "users": users
    }
    res["data"] = data
    return res


def tag_migrate(limit=10):
    res = {
        "meta": {
            "exported_on": cur_timestamp(),
            "version": "003"
        }
    }
    #coll = get_collection('test', 'articles')
    coll = get_collection('test', 'code')

    posts = []
    tags_id_map = {}
    posts_tags = []
    tag_id = 1000
    index = 0

    for doc in coll.find().batch_size(1000):
        #print(doc.get('title'))
        index += 1
        if index > limit:
            break

        posts.append(replace_post(doc))
        post_id = int(doc['source_url'].rsplit('/', 1)[1].split('.')[0])
        tag_list = doc.get('tag_list')
        tag = tag_list[0] if tag_list else ''
        tag = remove_china_char(tag)
        if tag:
            save_tag = tag.replace(' ', '-').lower()
            save_tag = find_first_tag(save_tag)
            if len(save_tag) > 10:
                posts_tags.append(
                    {"tag_id": 1, "post_id": post_id}
                )
                continue

            if save_tag not in tags_id_map:
                tag_id += 1
                tags.append({
                    "id": tag_id,
                    "name": save_tag,
                    "slug": save_tag,
                    "description": ""
                })
                tags_id_map[save_tag] = tag_id
                posts_tags.append(
                    {"tag_id": tags_id_map[save_tag], "post_id": post_id}
                )
            else:
                posts_tags.append(
                    {"tag_id": tags_id_map[save_tag], "post_id": post_id}
                )

    data = {
        "posts": posts,
        "tags": tags,
        "posts_tags": posts_tags,
        "users": users
    }
    res["data"] = data
    return res


def main():
    res = migrate(200)
    print(json.dumps(res, indent=4))

if __name__ == '__main__':
    #test()
    main()
