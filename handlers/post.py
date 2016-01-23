#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .base import BaseHandler
from tornado.web import HTTPError, url
from tornado.gen import coroutine
from models.post import Post
from models.user import User
from lib.html_tools import markdown2html


class IndexHandler(BaseHandler):
    @coroutine
    def get(self, page=1):
        limit = 10
        offset = limit * (page-1)
        posts = yield Post.objects.skip(offset).limit(limit)\
                      .order_by('-updated-at').find_all()
        posts_num = yield Post.objects.count()
        cur_page_num = 1
        all_page_num = int(posts_num/limit) + 1

        try:
            for post in posts:
                post.makrdown = markdown2html(post.markdown)
                del post.author.password
            self.render('index.html', posts=posts, cur_page=cur_page_num,
                        all_page_num=all_page_num)
        except Exception as e:
            print(e)


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
    url(r'/page/(\d+)?', IndexHandler),
    url(r'/post/(.*)', PostHandler),
]
