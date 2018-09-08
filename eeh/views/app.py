from flask import render_template, redirect, flash
from flask_login import current_user
from main import APP
from dbconnect import connection
from pymysql import escape_string


@APP.route('/app/')
def app():
    scouts = {}
    no_team = False
    con, conn = connection()
    sql = "SELECT id FROM scout_team WHERE scoutmaster_user_id = %s"
    if current_user.is_authenticated:
        scout_team_id = con.execute(sql, escape_string(str(current_user['id'])))
        if not scout_team_id == 0:
            sql = "SELECT * FROM scout WHERE id IN (SELECT id FROM scout_membership WHERE id IN (SELECT id FROM scouting_troop WHERE scout_team_id = %s))"
            scouts = con.execute(sql, escape_string(scout_team_id))
        no_team = True
    else:
        flash("Zaloguj się", "warning")
        return redirect('/')
    return render_template('app.html', harcerze=scouts, no_team=no_team)
