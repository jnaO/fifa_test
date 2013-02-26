import os
import sqlite3
from contextlib import closing
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash

# configuration
DATABASE = '/tmp/fifa.db'
DEBUGG = True
SECRET_KEY = '#Cr3un4Cup'
USERNAME = 'admin'
PASSWORD = 'demo123'

# App creation
fifa_app = Flask(__name__)
fifa_app.config.from_object(__name__)
# fifa_app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    """ Creates database tables """
    with closing(connect_db()) as db:
        with fifa_app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@fifa_app.before_request
def before_request():
    g.db = connect_db()

@fifa_app.teardown_request
def teardown_request(exception):
    g.db.close()

def connect_db():
    return sqlite3.connect(fifa_app.config['DATABASE'])


@fifa_app.route('/')
def show_entries():
    cur = g.db.execute('select _title, _text from entries order by _id desc')
    entries = [dict(_title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('db_tut/show_entries.html', entries=entries)


@fifa_app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(404)
    g.db.execute('insert into entries (_title, _text) values (?, ?)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@fifa_app.route('/login', methods=['GET, POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != fifa_app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != fifa_app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        return render_template('application/login.html', error=error)


@fifa_app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# @fifa_app.route('/<name>')
# def hello(name=None):
#     return render_template('path/test/hello.html', name=name)

@fifa_app.route('/history')
def history():
    return 'Past cups!'

@fifa_app.route('/history/<cup_name>')
def history_cup(cup_name):
    return render_template('history/past_cup.html', name=cup_name)
    return 'Cup %s!' % cup_name

# @fifa_app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return 'logged in'
#     else:
#         show_the_login_form()

if __name__ == '__main__':
    # fifa_app.debug = True
    port = int(os.environ.get('PORT', 5000))
    fifa_app.run(host='0.0.0.0', port=port)