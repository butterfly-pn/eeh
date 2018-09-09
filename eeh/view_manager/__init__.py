from flask_login import current_user
from flask import flash, request, redirect, url_for
from functools import wraps
from dbconnect import connection
from pymysql import escape_string

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Musisz być zalogowany", 'warning')
            next_url = request.url
            return redirect(url_for('login', next=next_url))
        return func(*args, **kwargs)
    return wrap

def scoutmaster_required(func):
    @wraps(func)
    @login_required
    def wrap(*args, **kwargs):
        con, conn = connection()
        is_scoutmaster = con.execute("SELECT * FROM scout_team WHERE scoutmaster_user_id = %s", escape_string(str(current_user['id_user'])))
        con.close()
        conn.close()
        if is_scoutmaster == 0:
            flash("Musisz być w komendzie", 'warning')
            return redirect(url_for('app'))
        return func(*args, **kwargs)
    return wrap


def komenda_required(func):
    @wraps(func)
    @login_required
    def wrap(*args, **kwargs):
        con, conn = connection()
        is_scoutmaster = con.execute(
            "SELECT a.id_scout, b.name, c.id_scout_team FROM scout a, scouting_troop b, scout_team c WHERE a.id_scout = %s AND b.name = \"Komenda\"", escape_string(str(current_user['scout_id'])))
        con.close()
        conn.close()
        if is_scoutmaster == 0:
            flash("Musisz być w komendzie", 'warning')
            return redirect(url_for('app'))
        return func(*args, **kwargs)
    return wrap
