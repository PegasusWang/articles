#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .base import BaseHandler
from tornado.web import HTTPError, url
from tornado.gen import coroutine
from models.post import Post
from models.user import User


class IndexHandler(BaseHandler):
    @coroutine
    def get(self, page=1):
        limit = 10
        offset = limit * (int(page)-1)
        posts = yield Post.objects.skip(offset).limit(limit)\
                          .order_by('updated_at').find_all()

        try:
            posts = [Post.to_dict(post) for post in posts]
            self.render('index.html', posts=posts, page=page,
                        next_page=str(int(page)+1))
        except Exception as e:
            print(e)
            self.render('index.html', posts=[], page=page,
                        next_page=str(int(page)+1))


class PostHandler(BaseHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user_id')

    @coroutine
    def get(self, slug):
        post_list = yield Post.objects.filter(slug=slug).find_all()
        if post_list:
            post = Post.to_dict(post_list[0])
            author = User.to_dict(post_list[0].author)
            self.render('post.html', post=post, author=author)
        else:
            raise HTTPError(404)

    def post(self):
        self.get_body_argument("title")


URL_ROUTES = [
    url(r'/', IndexHandler),
    url(r'/page/(\d+)/', IndexHandler),
    url(r'/post/(.*)', PostHandler),
]
