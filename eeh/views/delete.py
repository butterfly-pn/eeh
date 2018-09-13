from flask import request, redirect, flash
from eeh.view_manager.templating import render_template
from flask_login import current_user
from main import APP
from datetime import datetime
from eeh.view_manager import komenda_required
from dbconnect import connection
from pymysql import escape_string


@APP.route('/scout/<identifier>/delete/', methods=['GET'])
@komenda_required
def delete(identifier):
    con, conn = connection()
    sql = "SELECT a.id_scout, b.id_scout_membership, c.scout_team_id FROM scout a, scout_membership  b, scouting_troop c WHERE a.id_scout = %s AND a.id_scout = b.scout_id AND b.scouting_troop_id = c.id_scouting_troop AND c.scout_team_id IN (SELECT id_scout_team FROM scout_team WHERE scoutmaster_user_id = %s)"
    query = con.execute(sql, (escape_string(str(identifier)), escape_string(str(current_user['id_user']))))
    if query == 0:
        flash("Błędny identyfikator", 'warning')
    else:
        scout = con.fetchone()
        con.execute("SELECT id_status FROM status WHERE name = \"removed\"")
        status = con.fetchone()
        con.execute("UPDATE scout_membership SET status_id = %s WHERE id_scout_membership = %s", (escape_string(str(status['id_status'])), escape_string(scout['id_scout_membership'])))
    con.close()
    conn.close()
    return redirect('/')
