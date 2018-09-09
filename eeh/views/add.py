from flask import render_template, request, redirect, flash
from flask_login import current_user
from main import APP
from datetime import datetime
from eeh.view_manager import komenda_required
from dbconnect import connection
from pymysql import escape_string
from eeh.api.v1.scouting_troop import scouting_troop_join

def valid_pesel(pesel):
    if type(pesel) == str and len(pesel) == 11:
        return True
    return False

@APP.route('/add/', methods=["POST", "GET"])
@komenda_required
def add_get():
    if request.method == "GET":
        return render_template('add.html')
    elif request.method == "POST":
        try:
            print(request.form)
            con, conn = connection()
            if not valid_pesel(request.form['pesel']):
                flash("Zły pesel", 'warning')
                return redirect('/add/')
            sql = "INSERT INTO scout (first_name, middle_name, last_name, birthdate, pesel, address, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            con.execute(sql, (escape_string(request.form['first-name']), escape_string(request.form['middle-name']), escape_string(request.form['last-name']), escape_string(str(request.form['birthdate'])), escape_string(request.form['pesel']), escape_string(request.form['address']), escape_string(request.form['phone'])))
            conn.commit()
            scout_id = con.lastrowid
            con.execute("SELECT id_scouting_troop FROM scouting_troop WHERE scout_team_id IN (SELECT id_scout_team FROM scout_team WHERE scoutmaster_user_id= %s) AND name = \"none\"", escape_string(str(current_user['id_user'])))
            scouting_troop = con.fetchone()
            scouting_troop_join(scout_id, scouting_troop['id_scouting_troop'], notify=False)
            con.close()
            conn.close()
            flash("Dodano {} {}!".format(request.form['first-name'], request.form['last-name']), 'success')
        except Exception as error:
            flash("Error: " + str(error), 'danger')
        return redirect('/app/')
