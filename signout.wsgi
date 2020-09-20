import sys
sys.path.insert(0, '/usr/local/src/signout')

from signout import app as application
from signout import create_app, load_db_settings, dbuser, dbpassword, dbname, get_db
load_db_settings()
application = create_app()

# vim: ft=python:
