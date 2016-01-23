#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
from lib.html_tools import markdown2html
from tornado import gen
from tornado.util import ObjectDict
from .user import User
from motorengine.document import Document
from motorengine.fields import StringField, DateTimeField, IntField, ListField
from motorengine.fields.embedded_document_field import EmbeddedDocumentField
from motorengine.fields.reference_field import ReferenceField


class Post(Document):
    __collection__ = "Post"
    __lazy__ = False

    title = StringField()
    slug = StringField(unique=True)    # slug in url
    brief = StringField()
    image = StringField()    # first image url of post
    markdown = StringField()
    created_at = DateTimeField(auto_now_on_insert=True)    # datetime type
    updated_at = DateTimeField(auto_now_on_update=True)
    status_id = IntField()    # 0:deleted  1:published  2:draft
    #author = EmbeddedDocumentField(embedded_document_type=User)
    author = ReferenceField(reference_document_type=User)
    tags = ListField(StringField())   # Tag list

    @staticmethod
    def to_dict(post):
        """post is Post obj"""
        d = post.to_son()
        d['created_at'] = d['created_at'].strftime("%Y-%m-%d-%H")
        d['updated_at'] = d['updated_at'].strftime("%Y-%m-%d-%H")
        d['markdown'] = markdown2html(d['markdown'])
        return ObjectDict(d)
