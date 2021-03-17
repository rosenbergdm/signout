#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 David Rosenberg <dmr@davidrosenberg.me>
# Last updated Sat Feb 27 00:13:00 EST 2021
#
# Distributed under terms of the MIT license.

"""
signout/cli.py
Program to run the MSKCC intern signout page

"""

from signout.app import application as app
from signout.db import load_db_settings


def main():
    load_db_settings(app)
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
