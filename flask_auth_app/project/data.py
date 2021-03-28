from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user

data = Blueprint('data', __name__)

@data.route('/data')
@login_required
def index():
    return render_template('data.html')

# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', f_name=current_user.f_name, l_name=current_user.l_name, email=current_user.email)
