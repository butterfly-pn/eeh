from flask import render_template, redirect, flash, request
from flask_login import current_user
from main import APP
from dbconnect import connection
from pymysql import escape_string


@APP.route('/app/')
def app():
    scouts = []
    no_team = True
    con, conn = connection()
    sql = "SELECT id_scout_team, name FROM scout_team WHERE scoutmaster_user_id = %s"
    if current_user.is_authenticated:
        query = con.execute(sql, escape_string(str(current_user['id_user'])))
        scout_teams = con.fetchall()
        if not query == 0:
            sql = "SELECT a.id_scout, a.first_name, a.middle_name, a.last_name, a.birthdate, a.pesel, a.address, a.phone, b.scouting_troop_id, c.name as 'scouting_troop_name', c.scout_team_id FROM scout a, scout_membership b, scouting_troop c WHERE c.scout_team_id = %s AND b.scouting_troop_id = c.id_scouting_troop AND a.id_scout = b.scout_id"
            id = scout_teams[0]['id_scout_team']
            if request.args.get('scout-team'):
                query = con.execute("SELECT id_scout_team FROM scout_team WHERE id_scout_team = %s AND scoutmaster_user_id = %s",
                            (escape_string(request.args.get('scout-team')), escape_string(str(current_user['id_user']))))
                if not query == 0:
                    id = int(request.args.get('scout-team'))
            query = con.execute(sql, escape_string(str(id)))
            scouts_raw = con.fetchall()
            print(scouts_raw)
            if not query == 0:
                scouts = scouts_raw
            no_team = False
        con.close()
        conn.close()
    else:
        con.close()
        conn.close()
        flash("Zaloguj się", "warning")
        return redirect('/')
    return render_template('app.html', harcerze=scouts, no_team=no_team, scout_teams=scout_teams, current_scout_team_id=id)
