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
signout/app.py
MSKCC signout application app factory

"""
import os
import pkg_resources
from typing import Optional

from flask import Flask
from flask_talisman import Talisman


def create_app(appdir: Optional[str] = None):
    """
    Factory function to create the signout flask app.

    :param Optional[str]: Directory where the application is located

    :return: Flask application, secured with Talisman
    :rtype: flask.app.Flask
    """
    if appdir is None:
        appdir = os.path.dirname(
            pkg_resources.resource_filename(__name__, "dbsettings.json")
        )
        # appdir = os.path.dirname(os.path.realpath(__file__))
    app = Flask(__name__)
    app.config["SCRIPTDIR"] = appdir
    Talisman(app, content_security_policy=None)
    return app


application = create_app()


if __name__ == "__main__":
    pass
