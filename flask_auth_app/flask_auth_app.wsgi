#flask_auth_app.wsgi
import sys
sys.path.insert(0, '/var/www/html/flask_auth_app')

from project import app as application
