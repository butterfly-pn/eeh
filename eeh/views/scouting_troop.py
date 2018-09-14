from main import APP
from flask import session, request, redirect
from pymysql import escape_string
from dbconnect import connection
from eeh.view_manager import komenda_required
from eeh.view_manager.templating import render_template
from eeh.api.v1.scouting_troop import scouting_troop_create

@APP.route('/scouting-troops/', methods=['GET'])
@komenda_required
def scouting_troops_get():
    con, conn = connection()
    con.execute("SELECT * FROM scouting_troop WHERE scout_team_id = %s AND name <> \"none\"", escape_string(str(session['id_scout_team'])))
    scouting_troops = con.fetchall()
    con.close()
    conn.close()
    return render_template("scouting-troops.html", scouting_troops=scouting_troops)

@APP.route('/scouting-troops/', methods=['POST'])
@komenda_required
def scouting_troops_post():
    scouting_troop_create(request.form['name'], int(session['id_scout_team']))
    return redirect('/scouting-troops/')

@APP.route('/scouting-troop/<identifier>/', methods=['GET'])
@komenda_required
def scouting_troop_get(identifier):
    con, conn = connection()
    query = con.execute("SELECT * FROM scouting_troop WHERE id_scouting_troop = %s AND scout_team_id = %s",
                        (escape_string(identifier), escape_string(str(session['id_scout_team']))))
    scouting_troop = con.fetchone()
    if query == 0:
        return redirect("/scouting-troops/")
    con.execute("SELECT a.id_scout, a.first_name, a.last_name, b.name FROM scout a, scouting_troop b, scout_membership c WHERE b.id_scouting_troop = c.scouting_troop_id AND a.id_scout = c.scout_id AND b.scout_team_id = %s AND b.id_scouting_troop = %s",
                (escape_string(str(session['id_scout_team'])), escape_string(identifier)))
    scouts = con.fetchall()
    con.close()
    conn.close()
    return render_template("scouting-troop.html", scouts=scouts, scouting_troop=scouting_troop)
