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

from os import environ
from time import sleep
from twilio.rest import Client

import datetime
import json
import os
import pdb
import psycopg2
import re

# {{{ Defaults, dbsettings.json overrides this
DBNAME = ""
DBUSER = ""
DBPASSWORD = ""

ACCOUNT_SID = ""
AUTH_TOKEN = ""
FROM = ""

DEBUG_CALLBACKS = 0
DEBUG_TARGET_NUMBER = "+13125551212"
DEBUG_PRINT_NOT_MESSAGE = 0
DEBUG_SIGNOUT_OUTPUT = 0

# }}}


def load_settings():
    """
    Loads the database and twilio settings from the 'dbsettings.json' file in
    the project root directory

    """
    global DBNAME
    global DBUSER
    global DBPASSWORD
    global ACCOUNT_SID
    global AUTH_TOKEN
    global FROM
    global DEBUG_CALLBACKS
    global DEBUG_PRINT_NOT_MESSAGE
    global DEBUG_SIGNOUT_OUTPUT
    global DEBUG_TARGET_NUMBER
    if not "scriptdir" in globals():
        scriptdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    else:
        scriptdir = globals()["scriptdir"]
    fp = open(os.path.join(scriptdir, "dbsettings.json"))
    dbsettings = json.load(fp)
    fp.close()
    DBNAME = dbsettings["dbname"]
    DBUSER = dbsettings["username"]
    DBPASSWORD = dbsettings["password"]
    ACCOUNT_SID = dbsettings["twilio-sid"]
    AUTH_TOKEN = dbsettings["twilio-auth-token"]
    FROM = dbsettings["twilio-number"]
    if "DEBUG_CALLBACKS" in dbsettings.keys():
        if dbsettings["DEBUG_CALLBACKS"] in [0, 1]:
            DEBUG_CALLBACKS = dbsettings["DEBUG_CALLBACKS"]
    if "DEBUG_TARGET_NUMBER" in dbsettings.keys():
        if dbsettings["DEBUG_TARGET_NUMBER"].__len__() == 12:
            DEBUG_TARGET_NUMBER = dbsettings["DEBUG_TARGET_NUMBER"]
    if "DEBUG_SIGNOUT_OUTPUT" in dbsettings.keys():
        if dbsettings["DEBUG_SIGNOUT_OUTPUT"] in [0, 1]:
            DEBUG_SIGNOUT_OUTPUT = dbsettings["DEBUG_SIGNOUT_OUTPUT"]
    if "DEBUG_PRINT_NOT_MESSAGE" in dbsettings.keys():
        if dbsettings["DEBUG_PRINT_NOT_MESSAGE"] in [0, 1]:
            DEBUG_PRINT_NOT_MESSAGE = dbsettings["DEBUG_PRINT_NOT_MESSAGE"]
    for var in [
        "DBNAME",
        "DBUSER",
        "DBPASSWORD",
        "ACCOUNT_SID",
        "AUTH_TOKEN",
        "FROM",
        "DEBUG_CALLBACKS",
        "DEBUG_PRINT_NOT_MESSAGE",
        "DEBUG_SIGNOUT_OUTPUT",
        "DEBUG_TARGET_NUMBER",
    ]:
        globals()[var] = eval(var)


def get_notify_db():
    """
    Gets a new connection to the database

    :returns: Database connection
    :rtype: psycopg2.extensions.connection
    """
    conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASSWORD)
    return conn


def get_callback_number(nflist):
    """Get the phone number to text if there are missing signouts for a given list.

    :param str nflist: the night float list to get the callback number for (ex: "NF9132")

    :returns: The twilio-formatted callback to text (ex: '+13128675309')
    :rtype: str
    """

    conn = get_notify_db()
    cur = conn.cursor()
    dayofyear = datetime.datetime.today().timetuple().tm_yday
    cur.execute(
        """ SELECT callback FROM assignments INNER JOIN nightfloat ON assignments.nightfloat = nightfloat.id WHERE dayofyear = %s AND type = %s """,
        (dayofyear, nflist),
    )
    callback = cur.fetchall()
    if len(callback) > 0:
        callback = callback[0][0]
    else:
        callback = "+13125551212"
    cur.close()
    conn.close()
    if DEBUG_CALLBACKS:
        print(
            "DEBUG_CALLBACKS set -- would have returned '%s' but returning '%s' instead"
            % (callback, DEBUG_TARGET_NUMBER)
        )
        callback = DEBUG_TARGET_NUMBER
    return callback


def get_missing_signouts(nflist):
    """Get the active signouts that have not yet happened for the current day.

    :param str nflist: the night float list to get the missing signouts for (ex: "NF9132")

    :returns: a list of strings representing the names of the lists that haven't
        been signed out yet (ex: ["Breast, APP", "STR, Intern #1"]) or None if
        all lists are signed out
    :rtype: [str]

    """
    conn = get_notify_db()
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


def notify_missing_signouts(nflist):
    """
    Sends the text messages for missing signouts to the proper person, split
      into sms messages of <160 characters.

    :param str nflist: Nightfloat list to check and notify for (ex: "NF9132")

    :returns: Number of messages sent
    :rtype: int
    """

    missing_signouts = get_missing_signouts(nflist)
    if missing_signouts is not None:
        callback_number = get_callback_number(nflist)
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        if len(missing_signouts) <= 3:
            body = (
                "This is a notice from 'signout.mskcc.org'. "
                + "The following lists are not showing as submitted: "
                + "'"
                + "', '".join(missing_signouts)
                + "'"
            )
            if DEBUG_PRINT_NOT_MESSAGE:
                print(body)
            else:
                message = client.messages.create(
                    to=callback_number, from_=FROM, body=body
                )
        else:
            nmessages = int(len(missing_signouts) / 4) + 2
            if len(missing_signouts) % 4 == 0:
                nmessages -= 1
            body = (
                "This is notice (1/%s) from 'signout.mskcc.org'. " % str(nmessages)
                + "The following lists are not showing as submitted: "
            )
            if DEBUG_PRINT_NOT_MESSAGE:
                print(body)
            else:
                message = client.messages.create(
                    to=callback_number, from_=FROM, body=body
                )
            for i in range(nmessages - 1):
                sleep(1)
                mlist = missing_signouts[i * 4 : i * 4 + 4]
                body = (
                    "Notice (%s/%s): '" % (str(i + 2), str(nmessages))
                    + "', '".join(mlist)
                    + "'"
                )
                if DEBUG_PRINT_NOT_MESSAGE:
                    print(body)
                else:
                    message = client.messages.create(
                        to=callback_number, from_=FROM, body=body
                    )
    sleep(1)
    return nmessages


def notify_late_signup(signout_id, notify=True):
    """TODO: Send a text message to night float indicating that a 'late' addition
    to the signout list has occured

    :param int signout_id: DB id of the late signup

    :returns: none

    """
    conn = get_notify_db()
    cur = conn.cursor()
    cur.execute(
        """SELECT intern_name, service.name, intern_callback, type 
                    FROM signout
                    INNER JOIN service ON signout.service = service.id
                    WHERE signout.id = %s""",
        (signout_id,),
    )
    results = cur.fetchall()[0]
    cur.close()
    conn.close()

    callback_number = get_callback_number(results[3])
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    body = f"Notifying that the list {results[1]} was added when all other callbacks were complete.  Please call back {results[0]} at {results[2]}"
    if globals()["DEBUG_PRINT_NOT_MESSAGE"] == 1 or notify == False:
        print(body)
    else:
        body = client.messages.create(to=callback_number, from_=FROM, body=body)
    return


def notifier_main():
    """
    Run the notifier script.

    """
    nflists = ["NF9132", "NF9133"]
    total_messages = 0
    for nflist in nflists:
        total_messages += notify_missing_signouts(nflist)
    print("%s total SMS messages sent" % str(total_messages))
    return


if __name__ == "__main__":
    for v in ["DEBUG_CALLBACKS", "DEBUG_PRINT_NOT_MESSAGE"]:
        env_val = environ.get(v)
        if env_val:
            globals()[v] = int(env_val)
    load_settings()
    for v in ["ACCOUNT_SID", "AUTH_TOKEN", "FROM", "DEBUG_TARGET_NUMBER"]:
        env_val = environ.get(v)
        if env_val:
            globals()[v] = env_val
    notifier_main()
