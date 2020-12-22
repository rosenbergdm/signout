#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.

"""
notifier.py
Script to check whether patients are appropriately signed out
to night float nightly.  Meant to be run as a cron job.

"""

import datetime
import json
import os
import pdb
import psycopg2
import re

dbname = ""
dbuser = ""
dbpassword = ""


def load_db_settings():
    global dbname
    global dbuser
    global dbpassword
    scriptdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    fp = open(os.path.join(scriptdir, "dbsettings.json"))
    dbsettings = json.load(fp)
    fp.close()
    dbname = dbsettings["dbname"]
    dbuser = dbsettings["username"]
    dbpassword = dbsettings["password"]


def get_db():
    conn = psycopg2.connect(database=dbname, user=dbuser, password=dbpassword)
    return conn


def get_callback_number(nflist):
    """Get the phone number to text if there are missing signouts for a
    given list.

    Keyword arguments:
    nflist -- the night float list to get the callback number for (ex: "NF9132")

    Returns: --- a string representing the twilio-formatted callback to text
        (ex: '+13128675309')

    """

    conn = get_db()
    cur = conn.cursor()
    dayofyear = datetime.datetime.today().timetuple().tm_yday
    cur.execute(
        """
        SELECT callback 
        FROM assignments INNER JOIN nightfloat 
            ON assignments.nightfloat = nightfloat.id 
        WHERE dayofyear = %s
            AND type = %s """,
        (dayofyear, nflist),
    )
    callback = cur.fetchone()[0]
    return callback


if __name__ == "__main__":
    load_db_settings()
    notifier_main()
