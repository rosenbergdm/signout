#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
#    This file is part of signout.py the house staff web-based signout
#    manager for MSKCC.
#    Copyright © 2020-2021 David M. Rosenberg <dmr@davidrosenberg.me>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
signout/auth.py
Authorization setup and configuration for MSKCC signout program

"""

from flask_login import LoginManager
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired

from signout.app import application as app


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
        if username in cls.names:
            user_id = cls.names.index(username)
            return cls.get(user_id + 1)
        else:
            return None

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


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == "__main__":
    pass
