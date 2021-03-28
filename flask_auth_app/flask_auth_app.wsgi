#flask_auth_app.wsgi
import sys
sys.path.insert(0, '/var/www/html/flask_auth_app')

from flask_auth_app import main as application
