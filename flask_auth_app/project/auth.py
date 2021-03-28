from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from project.models import User
from . import db
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    f_name = request.form.get('f_name')
    l_name = request.form.get('l_name')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    print('username {}'.format(username))

    if user:
        flash('Email address already in use')
        return redirect(url_for('auth.signup'))

    new_user = User(username=username, \
            email=email, f_name=f_name, \
            l_name=l_name, \
            password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))
