from flask import render_template, request, redirect, flash
from flask_login import current_user
from pymysql import escape_string
from dbconnect import connection
from main import APP
from eeh.view_manager import login_required
from datetime import datetime
from eeh.api.v1.scouting_troop import *

@login_required
@APP.route('/scout-team/new/', methods=['GET'])
def scout_team_new_get():
    return render_template("scout-team-new.html")


@login_required
@APP.route('/scout-team/new/', methods=['POST'])
def scout_team_new_post():
    sql = "INSERT INTO scout_team (name, scoutmaster_user_id) VALUES (%s, {})".format(
        current_user['id'])
    con, conn = connection()
    con.execute(sql, escape_string(request.form['scout-team-name']))
    conn.commit()
    scout_team_id = con.lastrowid
    flash("Stworzono {}".format(request.form['scout-team-name']), 'success')
    scouting_troop_id = scouting_troop_create("Komenda", scout_team_id)
    scouting_troop_join(current_user['scout_id'], scouting_troop_id)
    con.close()
    conn.close()
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/app/')
