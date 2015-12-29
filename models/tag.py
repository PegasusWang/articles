#!/usr/bin/env python
# -*- coding:utf-8 -*-

from motorengine.document import Document
from motorengine.fields import StringField, IntField


class Tag(Document):
    id = IntField(required=True)
    name = StringField(required=True)
    slug = StringField(required=True)    # slug in url
    brief = StringField()


if __name__ == '__main__':
    main()
