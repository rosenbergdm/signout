#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 David Rosenberg <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.

"""
signout/notifier.py
Notifications module using twilio to send text messages

"""

import datetime
from time import sleep

from twilio.rest import Client

from signout.app import application as app
from signout.db import load_db_settings, get_db


def get_callback_number(nflist):
    """Get the phone number to text if there are missing signouts for a given list.

    :param str nflist: the night float list to get the callback number for (ex: "NF9132")

    :returns: The twilio_formatted callback to text (ex: '+13128675309')
    :rtype: str
    """

    conn = get_db()
    cur = conn.cursor()
    dayofyear = datetime.datetime.today().timetuple().tm_yday
    cur.execute(
        """ SELECT callback
              FROM assignments
             INNER JOIN nightfloat
                ON assignments.nightfloat = nightfloat.id
             WHERE dayofyear = %s
               AND type = %s""",
        (dayofyear, nflist),
    )
    callback = cur.fetchall()
    if len(callback) > 0:
        callback = callback[0][0]
    else:
        callback = "+17732403395"
    cur.close()
    conn.close()
    if app.config["DEBUG_CALLBACKS"]:
        print(
            "DEBUG_CALLBACKS set -- would have returned '%s' but returning '%s' instead"
            % (callback, app.config["DEBUG_TARGET_NUMBER"])
        )
        callback = app.config["DEBUG_TARGET_NUMBER"]
    return callback


def get_missing_signouts(nflist):
    """Get the active signouts that have not yet happened for the current day.

    :param str nflist: the night float list to get the missing signouts for (ex: "NF9132")

    :returns: a list of strings representing the names of the lists that haven't
        been signed out yet (ex: ["Breast, APP", "STR, Intern #1"]) or None if
        all lists are signed out
    :rtype: [str]

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
                   AND type = %s
               );""",
        (nflist, nflist),
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    if len(results) == 0:
        return None
    return [x[1] for x in results]


def notify_missing_signouts(nflist):
    """
    Sends the text messages for missing signouts to the proper person, split
      into sms messages of <160 characters.

    :param str nflist: Nightfloat list to check and notify for (ex: "NF9132")

    :returns: Number of messages sent
    :rtype: int
    """

    if (
        app.config["twilio_sid"] == ""
        or app.config["twilio_auth_token"] == ""
        or app.config["twilio_number"] == "+"
    ):
        print(
            "Skipping notifications as twilio configuration not set in dbsettings.json"
        )
        return 0

    missing_signouts = get_missing_signouts(nflist)
    if missing_signouts is not None:
        callback_number = get_callback_number(nflist)
        client = Client(app.config["twilio_sid"], app.config["twilio_auth_token"])

        if len(missing_signouts) <= 3:
            body = (
                "This is a notice from 'signout.mskcc.org'. "
                + "The following lists are not showing as submitted: "
                + "'"
                + "', '".join(missing_signouts)
                + "'"
            )
            if app.config["DEBUG_PRINT_NOT_MESSAGE"]:
                print(
                    "DEBUG_PRINT: Printing to stdout instead of sending text "
                    + "message since DEBUG_PRINT_NOT_MESSAGE=1 for message: "
                )
            else:
                client.messages.create(
                    to=callback_number, from_=app.config["twilio_number"], body=body
                )
        else:
            nmessages = int(len(missing_signouts) / 4) + 2
            if len(missing_signouts) % 4 == 0:
                nmessages -= 1
            body = (
                "This is notice (1/%s) from 'signout.mskcc.org'. " % str(nmessages)
                + "The following lists are not showing as submitted: "
            )
            if app.config["DEBUG_PRINT_NOT_MESSAGE"]:
                print(
                    "DEBUG_PRINT: Printing to stdout instead of sending "
                    + f"text message since DEBUG_PRINT_NOT_MESSAGE=1 for message: '{body}'"
                )
            else:
                client.messages.create(
                    to=callback_number, from_=app.config["twilio_number"], body=body
                )
            for i in range(nmessages - 1):
                sleep(1)
                mlist = missing_signouts[i * 4 : i * 4 + 4]
                body = (
                    "Notice (%s/%s): '" % (str(i + 2), str(nmessages))
                    + "', '".join(mlist)
                    + "'"
                )
                if app.config["DEBUG_PRINT_NOT_MESSAGE"]:
                    print(
                        "DEBUG_PRINT: Printing to stdout instead of sending "
                        + f"text message since DEBUG_PRINT_NOT_MESSAGE=1 for message: '{body}'"
                    )
                else:
                    client.messages.create(
                        to=callback_number, from_=app.config["twilio_number"], body=body
                    )
    sleep(1)
    return nmessages


def notifier_main():
    """
    Run the notifier script.

    """
    nflists = ["NF9132", "NF9133"]
    total_messages = 0
    for nflist in nflists:
        total_messages += notify_missing_signouts(nflist)
    print("%s total SMS messages sent" % str(total_messages))


def notify_late_signup(signout_id, notify=True):
    """TODO: Send a text message to night float indicating that a 'late' addition
    to the signout list has occured

    :param int signout_id: DB id of the late signup

    :returns: none

    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT intern_name,
               service.name,
               intern_callback,
               TYPE
          FROM signout
         INNER JOIN service
            ON signout.service = service.id
         WHERE signout.id = %s """,
        (signout_id,),
    )
    results = cur.fetchall()[0]
    cur.close()
    conn.close()

    if (
        app.config["twilio_sid"] == ""
        or app.config["twilio_auth_token"] == ""
        or app.config["twilio_number"] == "+"
    ):
        print(
            "Skipping notifications as twilio configuration not set in dbsettings.json"
        )
        return

    callback_number = get_callback_number(results[3])
    client = Client(app.config["twilio_sid"], app.config["twilio_auth_token"])
    body = (
        f"Notifying that the list {results[1]} was added when all other "
        + f"callbacks were complete.  Please call back {results[0]} at {results[2]}"
    )
    if app.config["DEBUG_PRINT_NOT_MESSAGE"] == 0 and notify:
        client.messages.create(
            to=callback_number, from_=app.config["twilio_number"], body=body
        )
    elif not notify:
        print(
            f"DEBUG_PRINT: Since notify=True, printing message rather than sending: {body}"
        )
    else:
        print(
            f"DEBUG_PRINT: Since DEBUG_PRINT_NOT_MESSAGE > 0, printing message rather than sending: {body}"
        )


if __name__ == "__main__":
    load_db_settings(app)
    notifier_main()
