#!/usr/bin/env python
# -*- coding:utf-8 -*-

from motorengine.document import Document
from motorengine.fields import StringField, DateTimeField, IntField, ListField


class Post(Document):
    id = IntField(required=True)
    title = StringField(required=True)
    slug = StringField(required=True)    # slug in url
    brief = StringField()
    image = StringField()    # first image url of post
    markdown = StringField(required=True)
    created_at = DateTimeField(auto_now_on_insert=True)    # datetime type
    updated_at = DateTimeField(auto_now_on_update=True)
    status_id = IntField(required=True)    # 0:deleted    1:published  2:draft
    author_id = IntField(required=True)
    tags = ListField(StringField())   # Tag list


if __name__ == '__main__':
    main()
