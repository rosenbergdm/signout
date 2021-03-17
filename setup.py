#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 David M. Rosenberg <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.


import atexit
import distutils.cmd
import distutils.log
import distutils.command.build
import os

import uuid

import setuptools
import setuptools.command.build_py
import setuptools.command.install
import jinja2
import psycopg2

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
        "SELECT datname FROM pg_database where datname=%s", (config_options["dbname"], )
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
        for opt in ["dbname", "dbuser", "dbpass"]:
            if opt in config_options.keys():
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
            if opt in config_options.keys():
                setattr(self, opt, config_options[opt])
        for opt in config_opt_names:
            if getattr(self, opt) != "":
                config_options[opt] = getattr(self, opt)
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
        atexit.register(post_install)

    def finalize_options(self):
        global config_options
        global config_opt_names
        print(f"config_options='{config_options}'")
        assert self.dbname != "", "'--dbname=DBNAME' is a required option"
        assert self.dbuser != "", "'--dbuser=DBUSER' is a required option"
        assert self.dbpass != "", "'--dbpass=DBPASS' is a required option"
        for opt in config_opt_names:
            if getattr(self, opt) != "":
                config_options[opt] = getattr(self, opt)
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
        "Flask==1.1.2",
        "flask-talisman==0.7.0",
        "Flask-WTF==0.14.3",
        "Flask-Login==0.5.0",
        "psycopg2==2.8.6",
        "twilio==6.53.0",
        "WTForms==2.3.3",
        "certifi==2020.12.5",
        "chardet==4.0.0",
        "click==7.1.2",
        "idna==2.10",
        "itsdangerous==1.1.0",
        "Jinja2==2.11.3",
        "MarkupSafe==1.1.1",
        "PyJWT==1.7.1",
        "pytz==2021.1",
        "requests==2.25.1",
        "six==1.15.0",
        "urllib3==1.26.3",
        "Werkzeug==1.0.1",
        "typing==3.7.4.3",
        "appdirs==1.4.4",
        "appnope==0.1.2",
        "astroid==2.5.1",
        "backcall==0.2.0",
        "black==20.8b1",
        "decorator==4.4.2",
        "greenlet==1.0.0",
        "ipdb==0.13.6",
        "ipython==7.21.0",
        "ipython-genutils==0.2.0",
        "isort==5.7.0",
        "jedi==0.18.0",
        "lazy-object-proxy==1.5.2",
        "mccabe==0.6.1",
        "msgpack==1.0.2",
        "mypy-extensions==0.4.3",
        "neovim==0.3.1",
        "parso==0.8.1",
        "pathspec==0.8.1",
        "pexpect==4.8.0",
        "pickleshare==0.7.5",
        "prompt-toolkit==3.0.17",
        "ptyprocess==0.7.0",
        "Pygments==2.8.1",
        "pylint==2.7.2",
        "pynvim==0.4.3",
        "regex==2020.11.13",
        "toml==0.10.2",
        "traitlets==5.0.5",
        "typed-ast==1.4.2",
        "typing-extensions==3.7.4.3",
        "wcwidth==0.2.5",
        "wrapt==1.12.1",
    ],
)
