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

from flask import Flask, current_app, g, url_for, render_template, redirect, app, request
import psycopg2

app = Flask(__name__)

def get_db():
    conn = psycopg2.connect(database = "signout", user = "davidrosenberg")
    return conn


@app.route('/')
def index():
    return redirect(url_for('submission'))

@app.route('/submission', methods=['GET', 'POST'])
def submission():
    conn = get_db()
    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM service where type='SOLID'")
        solid_services = [{'id': x[0], 'name': x[1]} for x in cur.fetchall()]
        cur.execute("SELECT id, name FROM service where type='LIQUID'")
        liquid_services = [{'id': x[0], 'name': x[1]} for x in cur.fetchall()]
        cur.execute("SELECT intern_name, name, addtime FROM signout LEFT JOIN service ON signout.service = service.id WHERE active is TRUE AND oncall is FALSE and type = 'SOLID' ORDER BY addtime ASC")
        noncall_solid_interns = [{'intern_name': x[0], 'name': x[1], 'addtime': x[2]} for x in cur.fetchall()]
        cur.execute("SELECT intern_name, name, addtime FROM signout LEFT JOIN service ON signout.service = service.id WHERE active is TRUE AND oncall is TRUE and type = 'SOLID' ORDER BY addtime ASC")
        call_solid_interns = [{'intern_name': x[0], 'name': x[1], 'addtime': x[2]} for x in cur.fetchall()]
        cur.execute("SELECT intern_name, name, addtime FROM signout LEFT JOIN service ON signout.service = service.id WHERE active is TRUE AND oncall is FALSE and type = 'LIQUID' ORDER BY addtime ASC")
        noncall_liquid_interns = [{'intern_name': x[0], 'name': x[1], 'addtime': x[2]} for x in cur.fetchall()]
        cur.execute("SELECT intern_name, name, addtime FROM signout LEFT JOIN service ON signout.service = service.id WHERE active is TRUE AND oncall is TRUE and type = 'LIQUID' ORDER BY addtime ASC")
        call_liquid_interns = [{'intern_name': x[0], 'name': x[1], 'addtime': x[2]} for x in cur.fetchall()]
        print(call_liquid_interns)
        cur.close()
        conn.close()
        return render_template('submission.html', solid_services=solid_services, liquid_services=liquid_services, noncall_solid_interns=noncall_solid_interns, call_solid_interns=call_solid_interns, noncall_liquid_interns=noncall_liquid_interns, call_liquid_interns=call_liquid_interns)
    else:
        cur = conn.cursor()
        cur.execute("INSERT INTO signout (intern_name, intern_callback, service, oncall) VALUES ('%s', '%s', %s, '%s')" %
                    (request.form['intern_name'], request.form['intern_callback'], request.form['service'], request.form['oncall']))
        conn.commit()
        cur.close()
        conn.close()
        return render_template("received.html")

if __name__ == "__main__":
    get_db()
    app.run(host="0.0.0.0")
