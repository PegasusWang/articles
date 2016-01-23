#!/usr/bin/env python
# -*- coding:utf-8 -*-

from motorengine.document import Document
from motorengine.fields import StringField, DateTimeField, IntField, EmailField
from tornado.util import ObjectDict


class User(Document):
    __collection__ = "User"

    name = StringField(required=True)
    password = StringField()
    slug = StringField(required=True, unique=True)    # slug in url
    email = EmailField(required=True, unique=True)
    created_at = DateTimeField(auto_now_on_insert=True)
    session = StringField()
    role_id = IntField()    # reader=10, writer=20, editor=30, root=40

    @staticmethod
    def to_dict(user):
        d = user.to_son()
        d['created_at'] = d['created_at'].strftime("%Y-%m-%d-%H")
        del d['password']
        return ObjectDict(d)
