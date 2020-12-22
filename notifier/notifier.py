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
    cur.close()
    conn.close()
    return callback


def get_missing_signouts(nflist):
    """Get the active signouts that have not yet happened for the current day.

    Keyword arguments:
    nflist -- the night float list to get the missing signouts for (ex: "NF9132")

    Returns -- a list of strings representing the names of the lists that haven't
        been signed out yet (ex: ["Breast, APP", "STR, Intern #1"]) or None if
        all lists are signed out

    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, name 
        FROM service 
        WHERE active IS true 
          AND type = %s 
          AND id NOT IN (
            SELECT service 
            FROM signout 
              INNER JOIN service 
                ON signout.service = service.id
            WHERE date_part('day', addtime) = date_part('day', current_timestamp)
              AND date_part('month', addtime) = date_part('month', current_timestamp)
              AND date_part('year', addtime) = date_part('year', current_timestamp) 
              AND type = %s);""",
        (nflist, nflist),
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    if len(results) == 0:
        return None
    else:
        return [x[1] for x in results]


if __name__ == "__main__":
    load_db_settings()
    notifier_main()
