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
from typing import Optional

from flask import Flask
from flask_talisman import Talisman


def create_app(appdir: Optional[str]=None):
    """
    Factory function to create the signout flask app.

    :param Optional[str]: Directory where the application is located

    :return: Flask application, secured with Talisman
    :rtype: flask.app.Flask
    """
    if appdir is None:
        appdir = os.path.dirname(os.path.realpath(__file__))
    app = Flask("signout")
    app.config["SCRIPTDIR"] = appdir
    Talisman(app, content_security_policy=None)
    return app


application = create_app()


if __name__ == "__main__":
    pass
