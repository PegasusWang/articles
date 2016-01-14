#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
from lib.html_tools import markdown2html
from tornado import gen
from motorengine.document import Document
from motorengine.fields import StringField, DateTimeField, IntField, ListField


class Post(Document):
    __collection__ = "Post"

    title = StringField()
    slug = StringField(unique=True)    # slug in url
    brief = StringField()
    image = StringField()    # first image url of post
    markdown = StringField()
    created_at = DateTimeField(auto_now_on_insert=True)    # datetime type
    updated_at = DateTimeField(auto_now_on_update=True)
    status_id = IntField()    # 0:deleted  1:published  2:draft
    author_id = StringField()
    tags = ListField(StringField())   # Tag list


def post_to_dict(post):
    """post is Post obj"""
    d = post.to_son()
    d['created_at'] = d['created_at'].strftime("%Y-%m-%d-%H")
    d['updated_at'] = d['updated_at'].strftime("%Y-%m-%d-%H")
    d['markdown'] = markdown2html(d['markdown'])
    return d
