#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 David M. Rosenberg <dmr@davidrosenberg.me>
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

from signout.app import application as app
from signout.db import load_db_settings
from signout.helpers import dbg
import signout.views

# pdb.set_trace()
