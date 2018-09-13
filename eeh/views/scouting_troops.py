from main import APP
from flask import render_template, session
from pymysql import escape_string
from dbconnect import connection
from eeh.view_manager import komenda_required

@APP.route('/scouting-troops/', methods=['GET'])
@komenda_required
def scouting_troops_get():
    con, conn = connection()
    con.execute("SELECT * FROM scouting_troop WHERE scout_team_id = %s AND name <> \"none\"", escape_string(str(session['id_scout_team'])))
    scouting_troops = con.fetchall()
    con.close()
    conn.close()
    return render_template("scouting-troops.html", scouting_troops=scouting_troops)
