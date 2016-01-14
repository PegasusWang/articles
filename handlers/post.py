#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .base import BaseHandler
from tornado.web import HTTPError, url
from tornado.gen import coroutine
from models.post import Post, post_to_dict
from models.user import User
from lib.html_tools import markdown2html


class PostHandler(BaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user_id')

    @coroutine
    def get(self, slug):
        post = yield Post.objects.filter(slug=slug).find_all()
        if post:
            post = post[0]
            post.markdown = markdown2html(post.markdown)
            user = yield User.objects.get(post.author_id)
            self.render('post.html', post=post, user=user)
        else:
            raise HTTPError(404)

    def post(self):
        self.get_body_argument("title")


URL_ROUTES = [
    url(r'/post/(.*)', PostHandler),
]
