#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 David M. Rosenberg <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.

"""
signout/db.py
MSKCC signout program database and configuration management

"""
import json
import os

import psycopg2

from signout.auth import User
from signout.app import application as app


def load_db_settings(app):
    with open(os.path.join(app.config["SCRIPTDIR"], "dbsettings.json")) as fp:
        dbsettings = json.load(fp)
    app.config["USERS"] = dict()
    for k in dbsettings:
        app.config[k] = dbsettings[k]
        if os.environ.get(k):
            app.config[k] = os.environ.get(k)
    for u in dbsettings["USERS"].keys():
        User(u, dbsettings["USERS"][u])
    app.config["SETTINGS_LOADED"] = 1
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


def get_db():
    conn = psycopg2.connect(
        database=app.config["DBNAME"],
        user=app.config["DBUSER"],
        password=app.config["DBPASSWORD"],
    )
    return conn


if __name__ == "__main__":
    pass