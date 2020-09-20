#!/usr/bin/env python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/usr/local/src/signout/')

from signout import app as application
from signout import load_db_settings
load_db_settings()
# application = create_app()

# vim: ft=python:
