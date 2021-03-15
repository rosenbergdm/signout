#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.

"""
signout/db.py
MSKCC signout program database and configuration management

"""
import json
import os
import pprint

import psycopg2
from flask import Flask, current_app

from auth import User
from helpers import dbg


def load_db_settings(app):
    with open(os.path.join(app.config["SCRIPTDIR"], "dbsettings.json")) as fp:
        dbsettings = json.load(fp)
    app.config["USERS"] = dict()
    for k in dbsettings:
        app.config[k] = dbsettings[k]
        if os.environ.get(k):
            e_val = os.environ.get(k)
            dbg(f"Setting '{k}' to '{e_val}' based on environment variable")
            app.config[k] = e_val
    for u in dbsettings["USERS"].keys():
        User(u, dbsettings["USERS"][u])
    app.config["SETTINGS_LOADED"] = 1
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


def get_db(app):
    conn = psycopg2.connect(
        database=app.config["DBNAME"],
        user=app.config["DBUSER"],
        password=app.config["DBPASSWORD"],
    )
    return conn


if __name__ == "__main__":
    pass
