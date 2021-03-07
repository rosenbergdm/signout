#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 Thomas Butterworth <dmr@davidrosenberg.me>
# Last updated Sat Feb 27 00:13:00 EST 2021
#
# Distributed under terms of the MIT license.

"""
signout.py
Program to run the MSKCC intern signout page

"""

import pprint
import sys

from flask import (
    Flask,
    url_for,
    render_template,
    redirect,
    request,
)
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from notifier.notifier import *

# This also ends up importing the follwing:
#   from os import environ
#   from time import sleep
#   from twilio.rest import Client

#   import datetime
#   import json
#   import os
#   import pdb
#   import psycopg2
#   import re

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
if "__file__" in dir():
    app.config["SCRIPTDIR"] = os.path.dirname(os.path.realpath(__file__))
else:
    if "SCRIPTDIR" in globals().keys():
        app.config["SCRIPTDIR"] = globals()["SCRIPTDIR"]
    if os.path.exists("/usr/local/src/signout/dbsettings.json"):
        app.config["SCRIPTDIR"] = "/usr/local/src/signout"
    elif os.path.exists(os.path.join(os.environ["HOME"], "src/signout")):
        app.config["SCRIPTDIR"] = os.path.join(os.environ["HOME"], "src/signout")
    else:
        raise Exception


CLEANUP_TIMESTAMP = re.compile(r"\.(..).*$")
SHIFT_TIMES = re.compile(r"^(\d{1,2})(:59:59\.)(.*)$")
app.config["USERS"] = dict()


@auth.verify_password
def verify_password(username, password):
    if username in app.config["USERS"] and check_password_hash(
        app.config["USERS"].get(username), password
    ):
        return username


def dbg(msg):
    if app.config["DEBUG_SIGNOUT_OUTPUT"]:
        pprint.pprint(msg, stream=sys.stderr)


def gen_med_sorter(intern_list):
    gen_med = []
    non_gen_med = []
    for i in intern_list:
        if i["name"][0:7] == "Gen Med":
            gen_med.append(i)
        else:
            non_gen_med.append(i)
    gen_med.extend(non_gen_med)
    return gen_med


def format_timestamp(ts):
    if ts == "None":
        return ""
    else:
        return CLEANUP_TIMESTAMP.sub(".\\1", ts)


def fix_earlytimes(ts):
    if SHIFT_TIMES.match(ts):
        hour = str(int(SHIFT_TIMES.sub("\\1", ts)) + 1).zfill(2)
        return str(hour) + SHIFT_TIMES.sub(":00:00.\\3", ts)
    else:
        return ts


def cleanup_date_input(ds):
    if "-" in ds:
        return ds
    else:
        parts = ds.split("/")
        ds = "-".join([parts[2], parts[0], parts[1]])
        return ds


def load_db_settings():
    fp = open(os.path.join(app.config["SCRIPTDIR"], "dbsettings.json"))
    dbsettings = json.load(fp)
    fp.close()
    for var in [
        "DBNAME",
        "DBUSER",
        "DBPASSWORD",
        "twilio-sid",
        "twilio-auth-token",
        "twilio-number",
        "DEBUG_CALLBACKS",
        "DEBUG_TARGET_NUMBER",
        "DEBUG_PRINT_NOT_MESSAGE",
        "DEBUG_SIGNOUT_OUTPUT",
        "DEBUG_PAGES",
    ]:
        if var in dbsettings:
            app.config[var] = dbsettings[var]
        else:
            print(f"Config missing setting '{var}'")
        if os.environ.get(var):
            e_val = os.environ.get(var)
            dbg(f"Setting '{var}' to '{e_val}' based on environment variable")
            app.config[var] = e_val
    app.config["USERS"].update(dbsettings["USERS"])


def get_db():
    conn = psycopg2.connect(
        database=app.config["DBNAME"],
        user=app.config["DBUSER"],
        password=app.config["DBPASSWORD"],
    )
    return conn


@app.route("/")
def index():
    return redirect(url_for("submission"))


@app.route("/start_signout", methods=["GET"])
def start_signout():
    signout_id = 0
    if request.args.get("id") is None:
        return "ERROR: Tried to start signout without an id query parameter for which signout db entry"
    try:
        signout_id = request.args.get("id")
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE signout set starttime=current_timestamp where id=%s"
            % str(signout_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return json.dumps({"id": signout_id, "status": "OK"})
    except Exception:
        return json.dumps({"id": signout_id, "status": "ERROR"})


@app.route("/nightfloat", methods=["GET", "POST"])
def nightfloat():
    if request.args.get("list") is None:
        listtype = "NF9132"
    else:
        listtype = request.args.get("list")
        # TODO: This is sort of dangerous.  Should do differently
    conn = get_db()
    if request.method == "GET":
        cur = conn.cursor()
        cur.execute(
            """
                    SELECT signout.id, intern_name, name, intern_callback 
                    FROM signout LEFT JOIN service 
                        ON signout.service = service.id 
                    WHERE signout.active is TRUE 
                        AND type = '%s' 
                        AND date_part('day', addtime) = date_part('day', current_timestamp) 
                        and date_part('month', addtime) = date_part('month', current_timestamp) 
                        and date_part('year', addtime) = date_part('year', current_timestamp)
                    ORDER BY addtime ASC
                    """
            % listtype.upper()
        )
        waiting_interns = gen_med_sorter(
            [
                {"id": x[0], "intern_name": x[1], "name": x[2], "intern_callback": x[3]}
                for x in cur.fetchall()
            ]
        )
        cur.execute(
            """
                    SELECT intern_name, name, intern_callback
                    FROM signout LEFT JOIN service 
                        ON signout.service = service.id 
                    WHERE signout.active is FALSE 
                        AND type = '%s'
                        AND date_part('day', addtime) = date_part('day', current_timestamp) 
                        and date_part('month', addtime) = date_part('month', current_timestamp) 
                        and date_part('year', addtime) = date_part('year', current_timestamp)
                    ORDER BY completetime ASC
                    """
            % listtype.upper()
        )
        completed_interns = [
            {"intern_name": x[0], "name": x[1], "intern_callback": x[2]}
            for x in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return render_template(
            "nightfloat.html",
            waiting_interns=waiting_interns,
            completed_interns=completed_interns,
            type=listtype,
            querystring="?list=" + listtype,
        )
    else:
        cur = conn.cursor()
        cur.execute(
            "UPDATE signout SET active = FALSE, completetime = current_timestamp WHERE id = %s"
            % request.form["signout.id"]
        )
        conn.commit()
        cur.close()
        conn.close()
        return render_template("removed.html", type=listtype)


def get_foreground_color(activestate):
    if activestate:
        return "#000000"
    else:
        return "#999999"


@app.route("/synctime")
def synctime():
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]


@app.route("/query", methods=["GET", "POST"])
def query():
    conn = get_db()
    if request.method == "GET":
        cur = conn.cursor()
        rangestring = "Showing signouts for %s" % (
            datetime.date.today() - datetime.timedelta(days=1)
        ).strftime("%m-%d-%Y")
        cur.execute(
            """
            SELECT intern_name, name, type, addtime::TIMESTAMP::TIME, starttime::TIMESTAMP, completetime::TIMESTAMP, addtime::TIMESTAMP::DATE as adddate
            FROM signout LEFT JOIN service 
                ON signout.service = service.id
            WHERE date_part('day', addtime) = date_part('day', current_timestamp - interval '1 day')
                and date_part('month', addtime) = date_part('month', current_timestamp)
                and date_part('year', addtime) = date_part('year', current_timestamp)
            ORDER BY completetime ASC"""
        )
        signoutlog = [
            {
                "intern_name": x[0],
                "name": x[1],
                "type": x[2],
                "addtime": fix_earlytimes(CLEANUP_TIMESTAMP.sub(".\\1", str(x[3]))),
                "starttime": x[4],
                "completetime": x[5],
                "adddate": x[6].strftime("%m-%d-%Y"),
                "elapsedtime": "",
            }
            for x in cur.fetchall()
        ]
        for idx in range(len(signoutlog)):
            sout = signoutlog[idx]
            try:
                timediff = sout["completetime"] - sout["starttime"]
                elapsed_minutes = int(timediff.seconds / 60)
                elapsed_seconds = timediff.seconds % 60
                sout["elapsedtime"] = "%i:%02d" % (elapsed_minutes, elapsed_seconds)
            except Exception:
                sout["elapsedtime"] = "Unable to be computed"
            if sout["starttime"] != None:
                sout["starttime"] = CLEANUP_TIMESTAMP.sub(
                    "", str(sout["starttime"].time())
                )
            else:
                sout["starttime"] = ""
            if sout["completetime"] != None:
                sout["completetime"] = CLEANUP_TIMESTAMP.sub(
                    "", str(sout["completetime"].time())
                )
            else:
                sout["completetime"] = ""
        cur.close()
        conn.close()
        return render_template(
            "query.html", signoutlog=signoutlog, rangestring=rangestring
        )
    else:
        cur = conn.cursor()
        if "NF9133" in request.form.keys():
            if "NF9132" in request.form.keys():
                typestring = ""
            else:
                typestring = " AND type = 'NF9133' "
        else:
            if "NF9132" in request.form.keys():
                typestring = " AND type = 'NF9132' "
            else:
                typestring = " AND type = 'notarealtype' "
        if request.form["addtime_date2"] == "":
            rangestring = "Showing signouts for %s" % request.form["addtime_date"]
            splitdate = cleanup_date_input(request.form["addtime_date"]).split("-")
            cur.execute(
                """
                SELECT intern_name, name, type, addtime::TIMESTAMP::TIME, starttime::TIMESTAMP, completetime::TIMESTAMP, addtime::TIMESTAMP::DATE as adddate
                FROM signout LEFT JOIN service 
                    ON signout.service = service.id
                WHERE date_part('day', addtime) = %s
                    and date_part('month', addtime) = %s
                    and date_part('year', addtime) = %s
                    %s
                ORDER BY completetime ASC"""
                % (splitdate[2], splitdate[1], splitdate[0], typestring)
            )
            dbg(cur.query)
        else:
            rangestring = "Showing signouts from %s to %s inclusive" % (
                request.form["addtime_date"],
                request.form["addtime_date2"],
            )
            splitdate = cleanup_date_input(request.form["addtime_date"]).split("-")
            splitenddate = cleanup_date_input(request.form["addtime_date2"]).split("-")
            cur.execute(
                """
                SELECT intern_name, name, type, addtime::TIMESTAMP::TIME, starttime::TIMESTAMP, completetime::TIMESTAMP, addtime::TIMESTAMP::DATE as adddate
                FROM signout LEFT JOIN service 
                    ON signout.service = service.id
                WHERE addtime BETWEEN
                    '"""
                + "-".join(splitdate)
                + """' and '"""
                + "-".join(splitenddate)
                + """'
                ORDER BY completetime ASC"""
            )
            dbg(cur.query)
        signoutlog = [
            {
                "intern_name": x[0],
                "name": x[1],
                "type": x[2],
                "addtime": fix_earlytimes(CLEANUP_TIMESTAMP.sub("", str(x[3]))),
                "starttime": x[4],
                "completetime": x[5],
                "adddate": x[6].strftime("%m-%d-%Y"),
                "elapsedtime": "",
            }
            for x in cur.fetchall()
        ]
        for idx in range(len(signoutlog)):
            sout = signoutlog[idx]
            try:
                timediff = sout["completetime"] - sout["starttime"]
                elapsed_minutes = int(timediff.seconds / 60)
                elapsed_seconds = timediff.seconds % 60
                sout["elapsedtime"] = "%i:%02d" % (elapsed_minutes, elapsed_seconds)
            except Exception:
                sout["elapsedtime"] = "Unable to be computed"
            if sout["starttime"] != None:
                sout["starttime"] = CLEANUP_TIMESTAMP.sub(
                    "", str(sout["starttime"].time())
                )
            else:
                sout["starttime"] = ""
            if sout["completetime"] != None:
                sout["completetime"] = CLEANUP_TIMESTAMP.sub(
                    "", str(sout["completetime"].time())
                )
            else:
                sout["completetime"] = ""
            signoutlog[idx] = sout
        cur.close()
        conn.close()
        return render_template(
            "query.html", signoutlog=signoutlog, rangestring=rangestring
        )


def submission_weekend():
    conn = get_db()
    if request.method == "GET":
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name FROM service where type='NF9132' AND active='t' ORDER BY name ASC"
        )
        solid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute(
            "SELECT id, name FROM service where type='NF9133' AND active='t' ORDER BY name ASC"
        )
        liquid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, signout.active, completetime - starttime as elapsedtime
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE date_part('day', addtime) = date_part('day', current_timestamp) 
                and date_part('month', addtime) = date_part('month', current_timestamp) 
                and date_part('year', addtime) = date_part('year', current_timestamp)
                and type = 'NF9132' 
            ORDER BY addtime ASC"""
        )
        noncall_solid_interns = [
            {
                "intern_name": x[0],
                "name": x[1],
                "addtime": fix_earlytimes(CLEANUP_TIMESTAMP.sub(".\\1", str(x[2]))),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
                "elapsedtime": format_timestamp(str(x[4])),
            }
            for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, signout.active, completetime - starttime as elapsedtime
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE date_part('day', addtime) = date_part('day', current_timestamp) 
                and date_part('month', addtime) = date_part('month', current_timestamp) 
                and date_part('year', addtime) = date_part('year', current_timestamp)
                and type = 'NF9133' 
            ORDER BY addtime ASC"""
        )
        noncall_liquid_interns = [
            {
                "intern_name": x[0],
                "name": x[1],
                "addtime": fix_earlytimes(CLEANUP_TIMESTAMP.sub(".\\1", str(x[2]))),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
                "elapsedtime": format_timestamp(str(x[4])),
            }
            for x in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return render_template(
            "submission_weekend.html",
            solid_services=solid_services,
            liquid_services=liquid_services,
            noncall_solid_interns=noncall_solid_interns,
            noncall_liquid_interns=noncall_liquid_interns,
        )
    else:
        cur = conn.cursor()
        if request.form.getlist("service") is None:
            return render_template("received.html")
        dbg(request.form)
        dbg(request.form.getlist("service"))
        for serviceid in request.form.getlist("service"):
            cur.execute(
                "INSERT INTO signout (intern_name, intern_callback, service, oncall, ipaddress, hosttimestamp) \
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (
                    request.form["intern_name"],
                    request.form["intern_callback"],
                    serviceid,
                    request.form["oncall"],
                    request.remote_addr,
                    request.form["hosttimestamp"],
                ),
            )
            callback_id = cur.fetchone()[0]
            conn.commit()
        cur.execute("SELECT type FROM service WHERE id = %s", (serviceid,))
        nflist = cur.fetchall()[0][0]
        cur.execute(
            """ SELECT Count(service.id)
                        FROM   signout
                               INNER JOIN service
                                       ON signout.service = service.id
                        WHERE  Date_part('day', addtime) = Date_part('day', CURRENT_TIMESTAMP)
                               AND Date_part('month', addtime) = Date_part('month', CURRENT_TIMESTAMP)
                               AND Date_part('year', addtime) = Date_part('year', CURRENT_TIMESTAMP)
                               AND signout.active = 't'
                               AND service.type = %s;""",
            (nflist,),
        )

        count = cur.fetchall()[0][0]
        cur.close()
        conn.close()
        timenow = datetime.datetime.now()
        if count < 2:
            if (
                (timenow.hour == 19 and timenow.minute > 30)
                or (timenow.hour > 19)
                or (timenow.hour < 12)
            ):
                notify_late_signup(callback_id)
        return render_template("received.html")


def submission_weekday():
    conn = get_db()
    if request.method == "GET":
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name FROM service where type='NF9132' AND active='t' ORDER BY name ASC"
        )
        solid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute(
            "SELECT id, name FROM service where type='NF9133' AND active='t' ORDER BY name ASC"
        )
        liquid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, signout.active, completetime - starttime as elapsedtime
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE date_part('day', addtime) = date_part('day', current_timestamp) 
                and date_part('month', addtime) = date_part('month', current_timestamp) 
                and date_part('year', addtime) = date_part('year', current_timestamp)
                AND oncall is FALSE 
                and type = 'NF9132' 
            ORDER BY addtime ASC"""
        )
        noncall_solid_interns = [
            {
                "intern_name": x[0],
                "name": x[1],
                "addtime": fix_earlytimes(CLEANUP_TIMESTAMP.sub(".\\1", str(x[2]))),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
                "elapsedtime": format_timestamp(str(x[4])),
            }
            for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, signout.active, completetime - starttime as elapsedtime
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE date_part('day', addtime) = date_part('day', current_timestamp) 
                and date_part('month', addtime) = date_part('month', current_timestamp) 
                and date_part('year', addtime) = date_part('year', current_timestamp)
                AND oncall is TRUE 
                and type = 'NF9132' 
            ORDER BY addtime ASC"""
        )
        call_solid_interns = [
            {
                "intern_name": x[0],
                "name": x[1],
                "addtime": fix_earlytimes(CLEANUP_TIMESTAMP.sub(".\\1", str(x[2]))),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
                "elapsedtime": format_timestamp(str(x[4])),
            }
            for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, signout.active, completetime - starttime as elapsedtime
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE date_part('day', addtime) = date_part('day', current_timestamp) 
                and date_part('month', addtime) = date_part('month', current_timestamp) 
                and date_part('year', addtime) = date_part('year', current_timestamp)
                AND oncall is FALSE 
                and type = 'NF9133' 
            ORDER BY addtime ASC"""
        )
        noncall_liquid_interns = [
            {
                "intern_name": x[0],
                "name": x[1],
                "addtime": fix_earlytimes(CLEANUP_TIMESTAMP.sub(".\\1", str(x[2]))),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
                "elapsedtime": format_timestamp(str(x[4])),
            }
            for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, signout.active, completetime - starttime as elapsedtime
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE date_part('day', addtime) = date_part('day', current_timestamp) 
                and date_part('month', addtime) = date_part('month', current_timestamp) 
                and date_part('year', addtime) = date_part('year', current_timestamp)
                AND oncall is TRUE 
                and type = 'NF9133' 
            ORDER BY addtime ASC"""
        )
        call_liquid_interns = [
            {
                "intern_name": x[0],
                "name": x[1],
                "addtime": fix_earlytimes(CLEANUP_TIMESTAMP.sub(".\\1", str(x[2]))),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
                "elapsedtime": format_timestamp(str(x[4])),
            }
            for x in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return render_template(
            "submission.html",
            solid_services=solid_services,
            liquid_services=liquid_services,
            noncall_solid_interns=noncall_solid_interns,
            call_solid_interns=call_solid_interns,
            noncall_liquid_interns=noncall_liquid_interns,
            call_liquid_interns=call_liquid_interns,
        )
    else:
        cur = conn.cursor()
        if request.form.getlist("service") is None:
            # This should never happen
            return render_template("received.html")
        dbg(request.form)
        dbg(request.form.getlist("service"))
        for serviceid in request.form.getlist("service"):
            cur.execute(
                """
                INSERT INTO
                  signout (
                    intern_name,
                    intern_callback,
                    service,
                    oncall,
                    ipaddress,
                    hosttimestamp
                  )
                VALUES
                  (%s, %s, %s, %s, %s, %s) RETURNING id;""",
                (
                    request.form["intern_name"],
                    request.form["intern_callback"],
                    serviceid,
                    request.form["oncall"],
                    request.remote_addr,
                    request.form["hosttimestamp"],
                ),
            )
            callback_id = cur.fetchone()[0]
            conn.commit()
        cur.execute("SELECT type FROM service WHERE id = %s", (serviceid,))
        nflist = cur.fetchall()[0][0]
        cur.execute(
            """ SELECT count(service.id)
                        FROM   signout
                               INNER JOIN service
                                       ON signout.service = service.id
                        WHERE  Date_part('day', addtime) = Date_part('day', CURRENT_TIMESTAMP)
                               AND Date_part('month', addtime) = Date_part('month', CURRENT_TIMESTAMP)
                               AND Date_part('year', addtime) = Date_part('year', CURRENT_TIMESTAMP)
                               AND signout.active = 't'
                               AND service.type = %s;""",
            (nflist,),
        )

        count = cur.fetchall()[0][0]
        cur.close()
        conn.close()
        timenow = datetime.datetime.now()
        if count < 2:
            if (
                (timenow.hour == 19 and timenow.minute > 30)
                or (timenow.hour > 19)
                or (timenow.hour < 12)
            ):
                notify_late_signup(callback_id)
        return render_template("received.html")


@app.route("/submission_weekday", methods=["GET", "POST"])
def debug_submission_weekday():
    if app.config["DEBUG_PAGES"]:
        return submission_weekday()
    return "NOT IN DEBUG MODE"


@app.route("/submission_weekend", methods=["GET", "POST"])
def debug_submission_weekend():
    if app.config["DEBUG_PAGES"]:
        return submission_weekend()
    return "NOT IN DEBUG MODE"


@app.route("/submission", methods=["GET", "POST"])
def submission():
    if datetime.datetime.now().isoweekday() > 5:
        return submission_weekend()
    return submission_weekday()


@app.route("/servicelist")
@auth.login_required
def servicelist():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        (SELECT id,
                name,
                type,
                active,
                (SELECT type AS othertype
                 FROM   service
                 WHERE  type != 'NF9132'
                 LIMIT  1) AS othertype
         FROM   service
         WHERE  type = 'NF9132'
         UNION
         SELECT id,
                name,
                type,
                active,
                (SELECT type AS othertype
                 FROM   service
                 WHERE  type != 'NF9133'
                 LIMIT  1) AS othertype
         FROM   service
         WHERE  type = 'NF9133')
        ORDER  BY id ASC;"""
    )
    results = cur.fetchall()
    slist = [
        {"id": x[0], "name": x[1], "type": x[2], "active": x[3], "othertype": x[4]}
        for x in results
    ]
    dbg(slist)
    return render_template("servicelist.html", servicelist=slist)


@app.route("/service")
@auth.login_required
def service():
    if request.args.get("id") is None or request.args.get("action") is None:
        dbg("MISSING ARGS")
        return redirect(url_for("servicelist"))
    else:
        service_id = int(request.args.get("id"))
        action = request.args.get("action")
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name FROM service WHERE id=%s ORDER BY id ASC", (service_id,)
    )
    slist = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
    service = slist[0]
    if app.config["DEBUG_SIGNOUT_OUTPUT"]:
        dbg(slist)
    msg = f"Setting '{service['name']}' (id #{service['id']}) to"
    if action == "activate":
        cur.execute(
            "UPDATE service set active = true where id = %s", (str(service_id),)
        )
        conn.commit()
        msg += f" ACTIVE"
    elif action == "deactivate":
        cur.execute(
            "UPDATE service set active = false where id = %s", (str(service_id),)
        )
        conn.commit()
        msg += f" INACTIVE"
    elif action == "set_type":
        newtype = request.args.get("newtype")
        cur.execute(
            "UPDATE service set type = %s where id = %s", (newtype, str(service_id))
        )
        conn.commit()
        msg += f" Night float list '{newtype}'"
    dbg({"msg": msg, "service": service, "slist": slist})
    cur.close()
    conn.close()
    return render_template("service.html", msg=msg, service=service)


@app.route("/admin")
@auth.login_required
def admin():
    return render_template("admin.html")


@app.route("/addservice", methods=["GET", "POST"])
@auth.login_required
def addservice():
    if request.method == "GET":
        return render_template("addservice.html")
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO SERVICE (name, type) VALUES (%s, %s) RETURNING id",
        (request.form["name"], request.form["nflist"]),
    )
    result = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return redirect(url_for("servicelist"))


if __name__ == "__main__":
    load_db_settings()
    app.run(host="0.0.0.0")
