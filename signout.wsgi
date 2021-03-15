#!/usr/bin/env python3
# Make sure you add WSGIPassAuthorization to the apache conf
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/usr/local/src/signout/')

from signout import app as application
from signout import load_db_settings
load_db_settings(application)
# application = create_app()

# vim: ft=python:
