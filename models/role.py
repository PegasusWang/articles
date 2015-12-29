#!/usr/bin/env python
# -*- coding:utf-8 -*-

from motorengine.document import Document
from motorengine.fields import StringField, DateTimeField, IntField


class RolesUsers(Document):
    user_id = IntField(required=True)
    role_id = IntField(required=True)


if __name__ == '__main__':
    main()
