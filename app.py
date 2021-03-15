#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.

"""
signout/app.py
MSKCC signout application app factory

"""
import os

from flask import Flask
from flask_talisman import Talisman


def create_app(appdir=None):
    if appdir is None:
        appdir = os.path.dirname(os.path.realpath(__file__))
    app = Flask("signout")
    app.config["SCRIPTDIR"] = appdir
    Talisman(app, content_security_policy=None)
    return app


application = create_app()


if __name__ == "__main__":
    pass
