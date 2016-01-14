#!/usr/bin/env python
# -*- coding:utf-8 -*-

from motorengine.document import Document
from motorengine.fields import StringField, DateTimeField, IntField, EmailField


class User(Document):
    name = StringField(required=True)
    slug = StringField(required=True, unique=True)    # slug in url
    email = EmailField(required=True, unique=True)
    created_at = DateTimeField(auto_now_on_insert=True)
    session = StringField(required=True, unique=True)
    role_id = IntField()    # reader=10, writer=20, editor=30, root=40
