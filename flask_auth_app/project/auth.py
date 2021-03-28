import datetime

import sqlalchemy as sal
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from project.models import User

from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/upload')
def upload():
    engine = connect_db()
    tables = engine.table_names()
    return render_template('upload.html', tables=tables)

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


@auth.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.form.get('tables'))
        if request.form.get('tables') == None:
            flash('Please Choose a Table to Add to')
            return redirect(url_for('auth.upload'))
        f = request.files['file']
        dbtable = request.form.get('tables')
        success = insert_file(f, dbtable)
        if success:
            return redirect(url_for('data.index'))
        else:
            flash('Something went wrong while uploading files')
            return redirect(url_for('auth.upload'))


def connect_db():
    server_name = 'cs5165-server.database.windows.net'
    database_name = 'midtermDB'

    username = 'dev'
    password = 'RFV1rfv!'

    engine = sal.create_engine(f'mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=SQL Server?Trusted_Connection=yes')
    return engine


def insert_file(file, db_table):
    engine = connect_db()
    a = file.read()
    row = a.decode("utf-8").split('\n')
    table = []
    for r in row:
        table.append(str(r).split(','))
    ints = ['HSHD_NUM', 'PRODUCT_NUM', 'BASKET_NUM', 'UNITS', 'WEEK_NUM', 'YEAR']
    date = 'PURCHASE'
    header = True
    header_str = ''
    Type = []
    for row in table:
        value_str = ''
        count = 0
        for col in row:
            if header:
                word = col.strip()
                if word.endswith('_'):
                    word = word[:-1]
                header_str += f'{word}, '
                if word in ints:
                    Type.append(2)
                elif word == date:
                    Type.append(1)
                else:
                    Type.append(0)
            else:
                if Type[count] == 2:
                    value_str += f'{col.strip()}, '
                elif Type[count] == 1:
                    date = datetime.datetime.strptime(col.strip(), '%d-%b-%y')
                    value_str += f'\'{date.date()}\', '
                else:
                    value_str += f'\'{col.strip()}\', '
                count += 1
        if header:
            header = False
        else:
            if value_str[:-2] != '':
                try:
                    engine.execute(f'INSERT INTO {db_table} ({header_str[:-2]}) VALUES ({value_str[:-2]})')
                except Exception as e:
                    print(e)
                    print(value_str)
                    return False
    return True
