#!/usr/bin/env python
# -*- coding:utf-8 -*-

from motorengine.document import Document
from motorengine.fields import StringField, DateTimeField, IntField, EmailField


class User(Document):
    id = IntField(required=True)
    name = StringField(required=True)
    slug = StringField(required=True)    # slug in url
    email = EmailField(required=True)
    created_at = DateTimeField(auto_now_on_insert=True)


if __name__ == '__main__':
    main()
