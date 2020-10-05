#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.

"""
signout.py 
Program to run the MSKCC intern signout page

"""

from flask import (
    Flask,
    current_app,
    g,
    url_for,
    render_template,
    redirect,
    app,
    request,
)
import datetime
import json
import os
import pdb
import psycopg2
import re

app = Flask(__name__)

dbname = ""
dbuser = ""
dbpassword = ""


def load_db_settings():
    global dbname
    global dbuser
    global dbpassword
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    fp = open(os.path.join(scriptdir, "dbsettings.json"))
    dbsettings = json.load(fp)
    fp.close()
    dbname = dbsettings["dbname"]
    dbuser = dbsettings["username"]
    dbpassword = dbsettings["password"]


def get_db():
    conn = psycopg2.connect(database=dbname, user=dbuser, password=dbpassword)
    return conn


@app.route("/")
def index():
    return redirect(url_for("submission"))


@app.route("/nightfloat", methods=["GET", "POST"])
def nightfloat():
    if request.args.get("list") is None:
        listtype = "NF9132"
    else:
        listtype = request.args.get("list")
    conn = get_db()
    if request.method == "GET":
        cur = conn.cursor()
        cur.execute(
            """
                    SELECT signout.id, intern_name, name, intern_callback 
                    FROM signout LEFT JOIN service 
                        ON signout.service = service.id 
                    WHERE active is TRUE 
                        AND type = '%s' 
                        AND date_part('day', addtime) = date_part('day', current_timestamp) 
                        and date_part('month', addtime) = date_part('month', current_timestamp) 
                        and date_part('year', addtime) = date_part('year', current_timestamp)
                    ORDER BY addtime ASC
                    """
            % listtype.upper()
        )
        waiting_interns = [
            {"id": x[0], "intern_name": x[1], "name": x[2], "intern_callback": x[3]}
            for x in cur.fetchall()
        ]
        cur.execute(
            """
                    SELECT intern_name, name 
                    FROM signout LEFT JOIN service 
                        ON signout.service = service.id 
                    WHERE active is FALSE 
                        AND type = '%s'
                        AND date_part('day', addtime) = date_part('day', current_timestamp) 
                        and date_part('month', addtime) = date_part('month', current_timestamp) 
                        and date_part('year', addtime) = date_part('year', current_timestamp)
                    ORDER BY completetime ASC
                    """
            % listtype.upper()
        )
        completed_interns = [
            {"intern_name": x[0], "name": x[1]} for x in cur.fetchall()
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


@app.route("/query", methods=["GET", "POST"])
def query():
    conn = get_db()
    cleanup_timestamp = re.compile(r"\..*$")
    if request.method == "GET":
        cur = conn.cursor()
        rangestring = "Showing signouts for %s" % datetime.date.today().strftime(
            "%Y-%M-%d"
        )
        cur.execute(
            """
            SELECT intern_name, name, type, addtime::TIMESTAMP::TIME, completetime::TIMESTAMP::TIME
            FROM signout LEFT JOIN service 
                ON signout.service = service.id
            WHERE date_part('day', addtime) = 4
                and date_part('month', addtime) = date_part('month', current_timestamp) 
                and date_part('year', addtime) = date_part('year', current_timestamp)
            ORDER BY completetime ASC"""
        )
        signoutlog = [
            {
                "intern_name": x[0],
                "name": x[1],
                "type": x[2],
                "addtime": cleanup_timestamp.sub("", str(x[3])),
                "completetime": cleanup_timestamp.sub("", str(x[4])),
                "elapsedtime": "",
            }
            for x in cur.fetchall()
        ]
        for idx in range(len(signoutlog)):
            if idx == len(signoutlog) - 1:
                signoutlog[idx]["elapsedtime"] = "Unable to be computed"
            else:
                begintime_raw = signoutlog[idx]["completetime"]
                if begintime_raw != "None":
                    begintime = datetime.datetime.strptime(begintime_raw, "%H:%M:%S")
                endtime_raw = signoutlog[idx + 1]["completetime"]
                if endtime_raw != "None":
                    endtime = datetime.datetime.strptime(endtime_raw, "%H:%M:%S")
                if begintime_raw != "None" and endtime_raw != "None":
                    timedelta = endtime - begintime
                    minutes = int(timedelta.seconds / 60)
                    seconds = timedelta.seconds - (minutes * 60)
                    signoutlog[idx]["elapsedtime"] = "%i:%02d" % (minutes, seconds)
                else:
                    signoutlog[idx]["elapsedtime"] = "Unable to be computed"
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
            splitdate = request.form["addtime_date"].split("-")
            cur.execute(
                """
                SELECT intern_name, name, type, addtime::TIMESTAMP::TIME, completetime::TIMESTAMP::TIME
                FROM signout LEFT JOIN service 
                    ON signout.service = service.id
                WHERE date_part('day', addtime) = %s
                    and date_part('month', addtime) = %s
                    and date_part('year', addtime) = %s
                    %s
                ORDER BY completetime ASC"""
                % (splitdate[2], splitdate[1], splitdate[0], typestring)
            )
        else:
            rangestring = "Showing signouts from %s to %s inclusive" % (
                request.form["addtime_date"],
                request.form["addtime_date2"],
            )
            splitdate = request.form["addtime_date"].split("-")
            splitenddate = request.form["addtime_date2"].split("-")
            cur.execute(
                """
                SELECT intern_name, name, type, addtime::TIMESTAMP::TIME, completetime::TIMESTAMP::TIME
                FROM signout LEFT JOIN service 
                    ON signout.service = service.id
                WHERE date_part('day', addtime) >= %s AND date_part('day', addtime) <= %s
                    and date_part('month', addtime) >= %s AND date_part('month', addtime) <= %s
                    and date_part('year', addtime) >= %s AND date_part('year', addtime) <= %s
                    %s
                ORDER BY completetime ASC"""
                % (
                    splitdate[2],
                    splitenddate[2],
                    splitdate[1],
                    splitenddate[1],
                    splitdate[0],
                    splitenddate[0],
                    typestring,
                )
            )
        signoutlog = [
            {
                "intern_name": x[0],
                "name": x[1],
                "type": x[2],
                "addtime": cleanup_timestamp.sub("", str(x[3])),
                "completetime": cleanup_timestamp.sub("", str(x[4])),
                "elapsedtime": "",
            }
            for x in cur.fetchall()
        ]

        for idx in range(len(signoutlog)):
            if idx == len(signoutlog) - 1:
                signoutlog[idx]["elapsedtime"] = "Unable to be computed"
            else:
                begintime_raw = signoutlog[idx]["completetime"]
                if begintime_raw != "None":
                    begintime = datetime.datetime.strptime(begintime_raw, "%H:%M:%S")
                endtime_raw = signoutlog[idx + 1]["completetime"]
                if endtime_raw != "None":
                    endtime = datetime.datetime.strptime(endtime_raw, "%H:%M:%S")
                if begintime_raw != "None" and endtime_raw != "None":
                    timedelta = endtime - begintime
                    minutes = int(timedelta.seconds / 60)
                    seconds = timedelta.seconds - (minutes * 60)
                    signoutlog[idx]["elapsedtime"] = "%i:%02d" % (minutes, seconds)
                else:
                    signoutlog[idx]["elapsedtime"] = "Unable to be computed"
        cur.close()
        conn.close()
        return render_template(
            "query.html", signoutlog=signoutlog, rangestring=rangestring
        )


@app.route("/submission", methods=["GET", "POST"])
def submission():
    conn = get_db()
    cleanup_timestamp = re.compile(r"\..*$")
    if request.method == "GET":
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM service where type='NF9132'")
        solid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute("SELECT id, name FROM service where type='NF9133'")
        liquid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, active
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
                "addtime": cleanup_timestamp.sub("", str(x[2])),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
            }
            for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, active
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
                "addtime": cleanup_timestamp.sub("", str(x[2])),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
            }
            for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, active
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
                "addtime": cleanup_timestamp.sub("", str(x[2])),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
            }
            for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime::TIMESTAMP::TIME, active
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
                "addtime": cleanup_timestamp.sub("", str(x[2])),
                "active": x[3],
                "fgcolor": get_foreground_color(x[3]),
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
        print(request.form)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO signout (intern_name, intern_callback, service, oncall) \
                    VALUES ('%s', '%s', %s, '%s')"
            % (
                request.form["intern_name"],
                request.form["intern_callback"],
                request.form["service"],
                request.form["oncall"],
            )
        )
        conn.commit()
        cur.close()
        conn.close()
        return render_template("received.html")


if __name__ == "__main__":
    load_db_settings()
    get_db()
    app.run(host="0.0.0.0")
