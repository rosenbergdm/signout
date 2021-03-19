#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
#    This file is part of signout.py the house staff web-based signout
#    manager for MSKCC.
#    Copyright © 2020-2021 David M. Rosenberg <dmr@davidrosenberg.me>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import atexit
import distutils.cmd
import distutils.command.build
import distutils.log
import os
import uuid

import jinja2
import psycopg2
import setuptools
import setuptools.command.build_py
import setuptools.command.install

config_options = {}
config_opt_names = [
    "dbname",
    "dbuser",
    "dbpass",
    "twilio_sid",
    "twilio_auth_token",
    "twilio_number",
]


def populate_database():
    global config_options
    conn = psycopg2.connect(
        user=config_options["dbuser"], password=config_options["dbpass"]
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(
        "SELECT datname FROM pg_database where datname=%s", (config_options["dbname"],)
    )
    if cur.fetchall() == []:
        cur.execute("CREATE DATABASE %s" % config_options["dbname"])
    else:
        conn.close()
        conn = psycopg2.connect(
            user=config_options["dbuser"],
            password=config_options["dbpass"],
            dbname=config_options["dbname"],
        )
        cur = conn.cursor()
        cur.execute(
            """SELECT ( SELECT count(id) FROM signout) + ( SELECT count(id) FROM assignments)"""
        )
        if cur.fetchall()[0][0] != 362:
            # I.E. not an empty database
            conn.close()
            raise Exception(f"{config_options['dbname']} IS NOT EMPTY")
    conn.close()
    conn = psycopg2.connect(
        user=config_options["dbuser"],
        password=config_options["dbpass"],
        dbname=config_options["dbname"],
    )
    cur = conn.cursor()
    with open(
        os.path.join(os.path.dirname("setup.py"), "src/signout/scripts/signout.sql")
    ) as fp:
        cur.execute(fp.read())
    conn.commit()
    conn.close()


def complete_template(src, dst, template_dict):
    with open(src) as fp:
        template = jinja2.Template(fp.read())
    with open(dst, "w") as fp:
        fp.write(template.render(**template_dict))


def post_install():
    global s
    scriptdir = os.path.join(s.command_obj["install"].install_lib, "signout")
    wsgifile = os.path.join(scriptdir, "signout.wsgi")
    complete_template("signout.wsgi.tmpl", wsgifile, {"pkgpath": scriptdir})


class ConfigureCommand(distutils.cmd.Command):
    """Setup package installation configuration"""

    description = "Setup Signout configuration"
    user_options = [
        ("dbname=", None, "name of postgreSQL database"),
        ("dbuser=", None, "name of postgreSQL user"),
        ("dbpass=", None, "password of postgreSQL user"),
        ("twilio-sid=", None, "twilio account SID"),
        ("twilio-auth-token=", None, "twilio authorizaton token"),
        ("twilio-number=", None, "twilio phone number"),
    ]

    def initialize_options(self):
        self.dbname = ""
        self.dbuser = ""
        self.dbpass = ""
        self.twilio_sid = ""
        self.twilio_auth_token = ""
        self.twilio_number = ""

    def finalize_options(self):
        global config_options
        global config_opt_names
        for opt in config_opt_names:
            if getattr(self, opt) != "":
                config_options[opt] = getattr(self, opt)
            elif opt in config_options.keys() and config_options[opt] != "":
                setattr(self, opt, config_options[opt])
        assert self.dbname != "", "'--dbname=DBNAME' is a required option"
        assert self.dbuser != "", "'--dbuser=DBUSER' is a required option"
        assert self.dbpass != "", "'--dbpass=DBPASS' is a required option"

    def run(self):
        tmpldict = {
            "dbname": self.dbname,
            "dbuser": self.dbuser,
            "dbpass": self.dbpass,
            "twilio_sid": self.twilio_sid,
            "twilio_auth_token": self.twilio_auth_token,
            "twilio_number": self.twilio_number,
            "secret_key": uuid.uuid4().hex,
        }
        tmpl_files = [
            ("dbsettings.json.tmpl", "src/signout/dbsettings.json"),
        ]

        for tmpl in tmpl_files:
            complete_template(tmpl[0], tmpl[1], tmpldict)
        populate_database()


class BuildCommand(distutils.command.build.build):
    """Custom build to ensure configuration occurs first"""

    user_options = (
        distutils.command.build.build.user_options + ConfigureCommand.user_options
    )

    def initialize_options(self):
        super().initialize_options()
        self.dbname = ""
        self.dbuser = ""
        self.dbpass = ""
        self.twilio_sid = ""
        self.twilio_auth_token = ""
        self.twilio_number = ""

    def finalize_options(self):
        global config_options
        global config_opt_names
        for opt in config_opt_names:
            if getattr(self, opt) != "":
                config_options[opt] = getattr(self, opt)
            elif opt in config_options.keys() and config_options[opt] != "":
                # elif config_options[opt] != "":
                setattr(self, opt, config_options[opt])
        assert self.dbname != "", "'--dbname=DBNAME' is a required option"
        assert self.dbuser != "", "'--dbuser=DBUSER' is a required option"
        assert self.dbpass != "", "'--dbpass=DBPASS' is a required option"
        super().finalize_options()

    def run(self):
        self.run_command("configure")
        super().run()


class InstallCommand(setuptools.command.install.install):

    user_options = (
        setuptools.command.install.install.user_options + ConfigureCommand.user_options
    )

    def initialize_options(self):
        super().initialize_options()
        self.dbname = ""
        self.dbuser = ""
        self.dbpass = ""
        self.twilio_sid = ""
        self.twilio_auth_token = ""
        self.twilio_number = ""

    def finalize_options(self):
        global config_options
        global config_opt_names
        for opt in config_opt_names:
            if getattr(self, opt) != "":
                config_options[opt] = getattr(self, opt)
                # elif config_options[opt] != "":
            elif opt in config_options.keys() and config_options[opt] != "":
                setattr(self, opt, config_options[opt])
        assert self.dbname != "", "'--dbname=DBNAME' is a required option"
        assert self.dbuser != "", "'--dbuser=DBUSER' is a required option"
        assert self.dbpass != "", "'--dbpass=DBPASS' is a required option"
        super().finalize_options()

    def run(self):
        self.run_command("build")
        super().run()


s = setuptools.setup(
    name="signout",
    cmdclass={
        "configure": ConfigureCommand,
        "build": BuildCommand,
        "install": InstallCommand,
    },
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "": [
            "src/signout/static",
            "src/signout/scripts",
            "src/signout/templates",
            "src/signout/dbsettings.json",
        ]
    },
    zip_safe=False,
    install_requires=[
        "Flask",
        "flask-talisman",
        "Flask-WTF",
        "Flask-Login",
        "psycopg2",
        "twilio",
        "WTForms",
        "certifi",
        "chardet",
        "click",
        "idna",
        "itsdangerous",
        "Jinja2",
        "MarkupSafe",
        "PyJWT",
        "pytz",
        "requests",
        "six",
        "urllib3",
        "Werkzeug",
        "typing",
        "appdirs",
        "appnope",
        "astroid",
        "backcall",
        "black",
        "decorator",
        "greenlet",
        "ipdb",
        "ipython",
        "ipython-genutils",
        "isort",
        "jedi",
        "lazy-object-proxy",
        "mccabe",
        "msgpack",
        "mypy-extensions",
        "neovim",
        "parso",
        "pathspec",
        "pexpect",
        "pickleshare",
        "prompt-toolkit",
        "ptyprocess",
        "Pygments",
        "pylint",
        "pynvim",
        "regex",
        "toml",
        "traitlets",
        "typing",
        "typed-ast",
        "typing-extensions",
        "wcwidth",
        "wrapt",
    ],
)

# try:
#     post_install()
# except Exception:
#     print("NO wsgi file written")
