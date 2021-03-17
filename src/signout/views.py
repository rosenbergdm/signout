#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 David M. Rosenberg <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.

"""
signout/views.py
MSKCC Signout program views and url routes

"""

import datetime
import json
import os
from shutil import copyfile

from flask import (
    abort,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
)
from werkzeug.security import check_password_hash

from signout.auth import (
    LoginForm,
    User,
)
from signout.app import application as app
from signout.db import get_db
from signout.helpers import (
    CLEANUP_TIMESTAMP,
    cleanup_date_input,
    dbg,
    fix_earlytimes,
    format_timestamp,
    gen_med_sorter,
    get_foreground_color,
    is_safe_url,
)
from signout.notifier import notify_late_signup, notify_missing_signouts


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form, meta={"csrf": False})
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.get_by_name(form.user_name.data)
            if user and User.check_password(user.user_name, form.rawpw.data):
                login_user(user, remember=True)
                flash("You were successfully logged in")
                next = request.args.get("next")
                if not is_safe_url(next):
                    return abort(400)
                return redirect(next or url_for("index"))
        else:
            flash("Invalid credentials")
    return render_template("login.html", form=form)


@login_required
@app.route("/logout", methods=["GET"])
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    flash("Logout successful")
    return redirect(url_for("index"))


@login_required
def verify_password(username, password):
    if username in app.config["USERS"] and check_password_hash(
        app.config["USERS"].get(username), password
    ):
        return username


@app.route("/")
@app.route("/index")
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
        cur.execute("""
                      SELECT signout.id,
                             intern_name,
                             name,
                             intern_callback
                        FROM signout
                        LEFT JOIN service
                          ON signout.service = service.id
                       WHERE signout.active IS TRUE
                         AND TYPE = '%s'
                         AND date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
                         AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
                         AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
                       ORDER BY addtime ASC"""
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
                    SELECT intern_name,
                           name,
                           intern_callback
                      FROM signout
                      LEFT JOIN service
                        ON signout.service = service.id
                     WHERE signout.active IS FALSE
                       AND TYPE = '%s'
                       AND date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
                       AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
                       AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
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
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE signout
           SET active = FALSE,
               completetime = CURRENT_TIMESTAMP
         WHERE id = %s"""
        % request.form["signout.id"]
    )
    conn.commit()
    cur.close()
    conn.close()
    return render_template("removed.html", type=listtype)


@app.route("/synctime")
def synctime():
    response = make_response(datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3])
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    return response


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
            SELECT intern_name,
                   name,
                   TYPE,
                   addtime::TIMESTAMP::TIME,
                   starttime::TIMESTAMP,
                   completetime::TIMESTAMP,
                   addtime::TIMESTAMP::DATE AS adddate
              FROM signout
              LEFT JOIN service
                ON signout.service = service.id
             WHERE date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP - interval '1 day')
               AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
               AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
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
                SELECT intern_name,
                       name,
                       TYPE,
                       addtime::TIMESTAMP::TIME,
                       starttime::TIMESTAMP,
                       completetime::TIMESTAMP,
                       addtime::TIMESTAMP::DATE AS adddate
                  FROM signout
                  LEFT JOIN service
                    ON signout.service = service.id
                 WHERE date_part('day', addtime) = %s
                   AND date_part('month', addtime) = %s
                   AND date_part('year', addtime) = %s %s
                 ORDER BY completetime ASC
                """
                % (splitdate[2], splitdate[1], splitdate[0], typestring)
            )
            # dbg(cur.query)
        else:
            rangestring = "Showing signouts from %s to %s inclusive" % (
                request.form["addtime_date"],
                request.form["addtime_date2"],
            )
            splitdate = cleanup_date_input(request.form["addtime_date"]).split("-")
            splitenddate = cleanup_date_input(request.form["addtime_date2"]).split("-")
            cur.execute(
                """
                SELECT intern_name,
                       name,
                       TYPE,
                       addtime::TIMESTAMP::TIME,
                       starttime::TIMESTAMP,
                       completetime::TIMESTAMP,
                       addtime::TIMESTAMP::DATE AS adddate
                  FROM signout
                  LEFT JOIN service
                    ON signout.service = service.id
                 WHERE addtime BETWEEN '"""
                + "-".join(splitdate)
                + """' and '"""
                + "-".join(splitenddate)
                + """'
                ORDER BY completetime ASC"""
            )
            # dbg(cur.query)
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
            SELECT intern_name,
                   name,
                   addtime::TIMESTAMP::TIME,
                   signout.active,
                   completetime - starttime AS elapsedtime
              FROM signout
              LEFT JOIN service
                ON signout.service = service.id
             WHERE date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
               AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
               AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
               AND TYPE = 'NF9132'
             ORDER BY addtime ASC
            """
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
            SELECT intern_name,
                   name,
                   addtime::TIMESTAMP::TIME,
                   signout.active,
                   completetime - starttime AS elapsedtime
              FROM signout
              LEFT JOIN service
                ON signout.service = service.id
             WHERE date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
               AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
               AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
               AND TYPE = 'NF9133'
             ORDER BY addtime ASC
            """
        )
        noncall_liquid_interns = gen_med_sorter(
            [
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
        )
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
        # dbg(request.form)
        # dbg(request.form.getlist("service"))
        for serviceid in request.form.getlist("service"):
            cur.execute(
                """
                INSERT INTO signout (intern_name, intern_callback, service, oncall, ipaddress, hosttimestamp)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                """,
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
            """
            SELECT count(distinct(hosttimestamp, intern_name))
              FROM signout
             INNER JOIN service
                ON signout.service = service.id
             WHERE date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
               AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
               AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
               AND signout.active = 't'
               AND service.type = %s; """,
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
            """
            SELECT id,
                   name
              FROM service
             WHERE TYPE='NF9132'
               AND active='t'
             ORDER BY name ASC
            """
        )
        solid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute(
            """
            SELECT id,
                   name
              FROM service
             WHERE TYPE='NF9133'
               AND active='t'
             ORDER BY name ASC"""
        )
        liquid_services = [{"id": x[0], "name": x[1]} for x in cur.fetchall()]
        cur.execute(
            """
            SELECT intern_name,
                   name,
                   addtime::TIMESTAMP::TIME,
                   signout.active,
                   completetime - starttime AS elapsedtime
              FROM signout
              LEFT JOIN service
                ON signout.service = service.id
             WHERE date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
               AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
               AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
               AND oncall IS FALSE
               AND TYPE = 'NF9132'
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
            SELECT intern_name,
                   name,
                   addtime::TIMESTAMP::TIME,
                   signout.active,
                   completetime - starttime AS elapsedtime
              FROM signout
              LEFT JOIN service
                ON signout.service = service.id
             WHERE date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
               AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
               AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
               AND oncall IS TRUE
               AND TYPE = 'NF9132'
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
            SELECT intern_name,
                   name,
                   addtime::TIMESTAMP::TIME,
                   signout.active,
                   completetime - starttime AS elapsedtime
              FROM signout
              LEFT JOIN service
                ON signout.service = service.id
             WHERE date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
               AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
               AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
               AND oncall IS FALSE
               AND TYPE = 'NF9133'
             ORDER BY addtime ASC"""
        )
        noncall_liquid_interns = gen_med_sorter(
            [
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
        )
        cur.execute(
            """
            SELECT intern_name,
                   name,
                   addtime::TIMESTAMP::TIME,
                   signout.active,
                   completetime - starttime AS elapsedtime
              FROM signout
              LEFT JOIN service
                ON signout.service = service.id
             WHERE date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
               AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
               AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
               AND oncall IS TRUE
               AND TYPE = 'NF9133'
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
        # dbg(request.form)
        # dbg(request.form.getlist("service"))
        for serviceid in request.form.getlist("service"):
            cur.execute(
                """
                INSERT INTO signout (intern_name, intern_callback, service, oncall, ipaddress, hosttimestamp)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
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
            """
            SELECT count(distinct(hosttimestamp, intern_name))
              FROM signout
             INNER JOIN service
                ON signout.service = service.id
             WHERE date_part('day', addtime) = date_part('day', CURRENT_TIMESTAMP)
               AND date_part('month', addtime) = date_part('month', CURRENT_TIMESTAMP)
               AND date_part('year', addtime) = date_part('year', CURRENT_TIMESTAMP)
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
@login_required
def debug_submission_weekday():
    return submission_weekday()


@app.route("/submission_weekend", methods=["GET", "POST"])
@login_required
def debug_submission_weekend():
    return submission_weekend()


@app.route("/submission", methods=["GET", "POST"])
def submission():
    if datetime.datetime.now().isoweekday() > 5:
        return submission_weekend()
    return submission_weekday()


def update_config(cfgvar, value, write_file=True):
    if write_file:
        with open(os.path.join(app.config["SCRIPTDIR"], "dbsettings.json")) as fp:
            dbconfig = json.load(fp)
        if cfgvar in dbconfig.keys():
            dbconfig[cfgvar] = value
            bkupfile = os.path.join(
                app.config["SCRIPTDIR"],
                f"dbsettings.{datetime.datetime.now().strftime('%s')}.json",
            )
            copyfile(os.path.join(app.config["SCRIPTDIR"], "dbsettings.json"), bkupfile)
            with open(
                os.path.join(app.config["SCRIPTDIR"], "dbsettings.json"), "w"
            ) as fp:
                json.dump(dbconfig, fp, indent=2)
    app.config[cfgvar] = value
    return dbconfig


@app.route("/servicelist")
@login_required
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
    return render_template("servicelist.html", servicelist=slist)


@app.route("/service")
@login_required
def service():
    if request.args.get("id") is None or request.args.get("action") is None:
        # dbg("MISSING ARGS")
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
    # dbg(slist)
    msg = f"Setting '{service['name']}' (id #{service['id']}) to"
    if action == "activate":
        cur.execute(
            "UPDATE service set active = true where id = %s", (str(service_id),)
        )
        conn.commit()
        msg += " ACTIVE"
    elif action == "deactivate":
        cur.execute(
            "UPDATE service set active = false where id = %s", (str(service_id),)
        )
        conn.commit()
        msg += " INACTIVE"
    elif action == "set_type":
        newtype = request.args.get("newtype")
        cur.execute(
            "UPDATE service set type = %s where id = %s", (newtype, str(service_id))
        )
        conn.commit()
        msg += f" Night float list '{newtype}'"
    # dbg({"msg": msg, "service": service, "slist": slist})
    cur.close()
    conn.close()
    return render_template("service.html", msg=msg, service=service)


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


@app.route("/addservice", methods=["GET", "POST"])
@login_required
def addservice():
    if request.method == "GET":
        return render_template("addservice.html")
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO SERVICE (name, type) VALUES (%s, %s) RETURNING id",
        (request.form["name"], request.form["nflist"]),
    )
    cur.fetchone()[0]
    conn.commit()
    conn.close()
    return redirect(url_for("servicelist"))


@app.route("/config", methods=["GET", "POST"])
@login_required
def configpage():
    if request.method == "POST":
        if request.args.get("var") is None or request.args.get("val") is None:
            return jsonify({"Success": False, "message": "var and val required"})
        else:
            var = request.args.get("var")
            val = request.args.get("val")
            if val.isnumeric():
                val = int(val)
            elif val.upper() == "TRUE":
                val = True
            elif val.upper() == "FALSE":
                val = False
        return jsonify(update_config(var, val))
    with open(os.path.join(app.config["SCRIPTDIR"], "dbsettings.json")) as fp:
        dbconfig = json.load(fp)
    if request.args.get("full") is None or request.args.get("full").upper() != "TRUE":
        cfg = {x: app.config[x] for x in dbconfig.keys()}
    else:
        cfg = dict(app.config)
    for k in ["PERMANENT_SESSION_LIFETIME", "SEND_FILE_MAX_AGE_DEFAULT"]:
        if k in cfg and isinstance(cfg[k], datetime.timedelta):
            cfg[k] = str(cfg[k])
    for k in ["DBPASSWORD", "SECRET_KEY", "twilio_sid", "twilio_auth_token"]:
        cfg[k] = "******"
    if "USERS" in cfg:
        for k in cfg["USERS"]:
            cfg["USERS"][k] = "******"
    return jsonify(cfg)


@app.route("/notifynightfloat")
def send_missing_signouts():
    if request.args.get("key") is None:
        return jsonify({"Success": False, "Message": "key is required"})
    if check_password_hash(request.args.get("key"), app.config["SECRET_KEY"]):
        notify_missing_signouts("NF9132")
        notify_missing_signouts("NF9133")
        return jsonify({"Success": True})
    return jsonify({"Success": False, "Message": "key mismatch"})


if __name__ == "__main__":
    pass
