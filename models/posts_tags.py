#!/usr/bin/env python
# -*- coding:utf-8 -*-

from motorengine.document import Document
from motorengine.fields import StringField, DateTimeField, IntField


class PostsTags(Document):
    tag_id = IntField(required=True)
    post_id = IntField(required=True)
