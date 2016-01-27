#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bcrypt
from motorengine.document import Document
from motorengine.fields import StringField, DateTimeField, IntField, EmailField
from tornado.escape import utf8
from tornado.util import ObjectDict


class User(Document):
    __collection__ = "User"

    name = StringField(required=True)
    password_hash = StringField(on_save=lambda user, creating:
                                bcrypt.hashpw(utf8(user.password_hash),
                                              bcrypt.gensalt()))    # gen hash
    slug = StringField(required=True, unique=True)    # slug in url
    email = EmailField(required=True, unique=True)
    created_at = DateTimeField(auto_now_on_insert=True)
    session = StringField()
    role_id = IntField()    # reader=10, writer=20, editor=30, root=40

    def to_dict(self):
        d = self.to_son()
        d['created_at'] = d['created_at'].strftime("%Y-%m-%d")
        del d['password_hash']
        return ObjectDict(d)

    def check_password(self, to_check_password):
        return self.password_hash == bcrypt.hashpw(utf8(to_check_password),
                                                   utf8(self.password_hash))
