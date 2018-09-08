from flask import render_template, request, redirect, flash
from flask_login import current_user
from pymysql import escape_string
from dbconnect import connection
from main import APP
from eeh.view_manager import login_required
from datetime import datetime

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
    sql = "INSERT INTO scouting_troop (name, scout_team_id) VALUES (\"Komenda\", {})".format(scout_team_id)
    con.execute(sql)
    conn.commit()
    scouting_troop_id = con.lastrowid
    flash("Stworzono \"Komenda\" w {}".format(request.form['scout-team-name']), 'success')
    sql = "INSERT INTO scout_membership (scout_id, scouting_troop_id, date) VALUES ({}, {}, %s)".format(current_user['scout_id'], scouting_troop_id)
    con.execute(sql, escape_string(str(datetime.now())))
    conn.commit()
    flash("Dołączono do \"Komenda\" w {}".format(
        request.form['scout-team-name']), 'success')
    con.close()
    conn.close()
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/app/')
