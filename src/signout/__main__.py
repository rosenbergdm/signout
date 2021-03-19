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
signout/__main__.py
Program to run the MSKCC intern signout page

Run this as `> python3 -m signout`
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from signout.app import application as app
from signout.db import load_db_settings


if __name__ == "__main__":
    load_db_settings(app)
    app.run(host="0.0.0.0", debug=True)
