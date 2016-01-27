#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import _env
from .base import BaseHandler
from models.forms import RegisterForm, LoginForm
from models.user import User
from tornado.web import authenticated, url
from tornado.gen import coroutine
from slugify import slugify


class UserBaseHandler(BaseHandler):
    def get_current_user(self):
        # Do not use get_secure_cookie('use_id', 0)
        return self.get_secure_cookie('user_id')


class UserMainHandler(UserBaseHandler):
    @authenticated
    def get(self):
        self.render('/user/index.html', user=self.current_user)


class UserRegisterHandler(UserBaseHandler):
    def get(self):
        self.render('/login.html', errors="")

    @coroutine
    def post(self):
        form = RegisterForm(self.request.arguments)
        if form.validate():
            print('validate success')
            user = yield User.objects.create(name=form.data['username'],
                                        slug=slugify(form.data['username']),
                                        email=form.data['email'],
                                        password_hash=form.data['password'])
        else:
            print('register error')
            self.render('/login.html', errors=form.errors)
            return
        self.set_secure_cookie("user_id", str(user._id))
        #self.redirect(self.get_argument('next', '/'))
        self.redirect('/')


class UserLoginHandler(UserBaseHandler):
    def get(self):
        self.render('/login.html', errors="")

    @coroutine
    def post(self):
        form = LoginForm(self.request.arguments)
        if form.validate():
            email = form.data['email']
            pwd = form.data['password']
            user = yield User.objects.filter(email=email).find_all()
            if not user or (not user[0].check_password(pwd)):
                self.render('/login.html', errors="Invalid email or password")
                return
            if form.data['remeber_me']:
                self.set_secure_cookie("user_id", str(user[0]._id))
            self.redirect(self.get_argument('next', '/'))

        else:
            self.render('/login.html', errors="Invalid email or password")
            return


class UserLogoutHandler(UserBaseHandler):
    def get(self):
        self.clear_cookie("user_id")
        self.redirect(self.get_argument("next", "/"))


URL_ROUTES = [
    url(r'/login', UserLoginHandler),
    url(r'/register', UserRegisterHandler),
    url(r'/logout', UserLogoutHandler),
]
