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
import json
import os
import psycopg2

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
        listtype = "Solid"
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
        return str(request.form)


@app.route("/submission", methods=["GET", "POST"])
def submission():
    conn = get_db()
    if request.method == "GET":
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM service where type='SOLID'")
        solid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute("SELECT id, name FROM service where type='LIQUID'")
        liquid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute(
            """
            SELECT intern_name, name, addtime 
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE active is TRUE 
                AND oncall is FALSE 
                and type = 'SOLID' 
            ORDER BY addtime ASC"""
        )
        noncall_solid_interns = [
            {"intern_name": x[0], "name": x[1], "addtime": x[2]} for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime 
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE active is TRUE 
                AND oncall is TRUE 
                and type = 'SOLID' 
            ORDER BY addtime ASC"""
        )
        call_solid_interns = [
            {"intern_name": x[0], "name": x[1], "addtime": x[2]} for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime 
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE active is TRUE 
                AND oncall is FALSE 
                and type = 'LIQUID' 
            ORDER BY addtime ASC"""
        )
        noncall_liquid_interns = [
            {"intern_name": x[0], "name": x[1], "addtime": x[2]} for x in cur.fetchall()
        ]
        cur.execute(
            """
            SELECT intern_name, name, addtime 
            FROM signout LEFT JOIN service 
                ON signout.service = service.id 
            WHERE active is TRUE 
                AND oncall is TRUE 
                and type = 'LIQUID' 
            ORDER BY addtime ASC"""
        )
        call_liquid_interns = [
            {"intern_name": x[0], "name": x[1], "addtime": x[2]} for x in cur.fetchall()
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
