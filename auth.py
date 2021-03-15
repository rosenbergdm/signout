#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 Thomas Butterworth <dmr@davidrosenberg.me>
# Last updated Sat Feb 27 00:13:00 EST 2021
#
# Distributed under terms of the MIT license.

"""
signout/auth.py
Authorization setup and configuration for MSKCC signout program

"""

from flask_login import (
    LoginManager,
    login_required,
    login_user,
    current_user,
    logout_user,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.security import check_password_hash, generate_password_hash


class LoginForm(FlaskForm):
    user_name = StringField(
        "Name: ", validators=[InputRequired("'Name' failed DataRequired")]
    )
    rawpw = PasswordField(
        "Password: ", validators=[InputRequired("InputRequired failed for 'rawpw'")]
    )

    def __repr__(self):
        return (
            f"LoginForm (user_name = {self.user_name.data}, rawpw = {self.rawpw.data})"
        )


class User(object):
    max_id = 0
    names = []
    users = []

    @classmethod
    def increment_id(cls):
        cls.max_id += 1
        return cls.max_id

    @classmethod
    def get_num_ids(cls):
        return cls.max_id

    @classmethod
    def get(cls, user_id):
        if type(user_id) is str:
            user_id = int(user_id)
        return cls.users[user_id - 1]

    @classmethod
    def get_by_name(cls, username):
        user_id = cls.names.index(username)
        return cls.get(user_id + 1)

    @classmethod
    def check_password(cls, user_name, rawpw):
        user = cls.get_by_name(user_name)
        if user:
            if check_password_hash(user.pwhash, rawpw):
                return user
        return None

    def __init__(self, user_name, pwhash="", user_id=None):
        if user_id is None:
            user_id = User.increment_id()
        self.user_id = user_id
        self.user_name = user_name
        self.pwhash = pwhash
        self.authenticated = False

        User.names.append(user_name)
        User.users.append(self)

    def __repr__(self):
        return (
            f"User: (user_name = '{self.user_name}', "
            + f"pwhash = '******', user_id={self.user_id}, "
            + f"authenticated={self.authenticated})"
        )

    def set_password(self, password, raw=True):
        if raw:
            self.pwhash = generate_password_hash(password)
        else:
            self.pwhash = password

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymouse(self):
        return False

    def get_id(self):
        return str(self.user_id)


if __name__ == "__main__":
    pass
