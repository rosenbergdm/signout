#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 Thomas Butterworth <dmr@davidrosenberg.me>
# Last updated Sat Feb 27 00:13:00 EST 2021
#
# Distributed under terms of the MIT license.

"""
signout/__init__.py
Program to run the MSKCC intern signout page

"""

__version__ = "0.9.9"

import os
import pdb

# from signout.auth import (
#     User,
#     LoginManager,
# )
from signout.app import application as app
from signout.helpers import dbg
import signout.views
# pdb.set_trace()


# SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)