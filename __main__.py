#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 Thomas Butterworth <dmr@davidrosenberg.me>
# Last updated Sat Feb 27 00:13:00 EST 2021
#
# Distributed under terms of the MIT license.

"""
signout/__main__.py
Program to run the MSKCC intern signout page

Run this as `> python3 -m signout`
"""

from signout.app import application as app
from signout.db import load_db_settings

# from signout.helpers import dbg

if __name__ == "__main__":
    load_db_settings(app)
    app.run(host="0.0.0.0", debug=True)
