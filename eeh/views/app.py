from flask import render_template, redirect, flash
from flask_login import current_user
from main import APP
from dbconnect import connection
from pymysql import escape_string


@APP.route('/app/')
def app():
    no_team = True
    con, conn = connection()
    sql = "SELECT id_scout_team FROM scout_team WHERE scoutmaster_user_id = %s"
    if current_user.is_authenticated:
        query = con.execute(sql, escape_string(str(current_user['id_user'])))
        scout_team = con.fetchone()
        if not query == 0:
            sql = "SELECT a.first_name, a.middle_name, a.last_name, a.birthdate, a.pesel, a.address, a.phone, b.name AS 'scouting_troop_name' FROM scout a, scouting_troop b WHERE id_scout IN (SELECT scout_id FROM scout_membership WHERE scouting_troop_id IN (SELECT id_scouting_troop FROM scouting_troop WHERE scout_team_id = %s))"
            query = con.execute(sql, escape_string(str(scout_team['id_scout_team'])))
            scouts_raw = con.fetchall()
            print(scouts_raw)
            if not query == 0:
                scouts = scouts_raw
            no_team = False
    else:
        flash("Zaloguj się", "warning")
        return redirect('/')
    return render_template('app.html', harcerze=scouts, no_team=no_team)
