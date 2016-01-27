#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""forms of user account"""


from .user import User
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length, \
    DataRequired, Regexp, EqualTo
from wtforms_tornado import Form
from wtforms import ValidationError
from tornado.gen import coroutine


class LoginForm(Form):
    email = StringField('email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('password', validators=[Required()])
    remeber_me = BooleanField('remeber_me')


class RegisterForm(Form):
    email = StringField('email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
               'username must have only letters, numbers, or underscores')])
    password = PasswordField('password', validators=[
        DataRequired(), EqualTo('password2', message='password must match.')])
    password2 = PasswordField('confirm password', validators=[DataRequired()])

    @coroutine
    def validate_email(self, field):
        users = yield User.objects.filter(email=field.data).find_all()
        if users:
            raise ValidationError('Email already registered.')

    @coroutine
    def validate_username(self, field):
        users = yield User.objects.filter(username=field.data).find_all()
        if users:
            raise ValidationError('Username already in use.')
