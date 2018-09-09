from flask import flash
from pymysql import escape_string
from dbconnect import connection
from datetime import datetime


def scouting_troop_join(scout_id, scouting_troop_id, notify=True):
    con, conn = connection()
    sql = "INSERT INTO scout_membership (scout_id, scouting_troop_id, date) VALUES (%s, %s, %s)"
    con.execute("SELECT name FROM scouting_troop WHERE id_scouting_troop = %s",
                escape_string(str(scouting_troop_id)))
    scouting_troop = con.fetchone()
    con.execute("SELECT first_name, last_name FROM scout WHERE id_scout = %s", escape_string(str(scout_id)))
    scout = con.fetchone()
    con.execute("SELECT name FROM scout_team WHERE id_scout_team IN (SELECT scout_team_id FROM scouting_troop WHERE id_scouting_troop = %s)",
                escape_string(str(scouting_troop_id)))
    scout_team = con.fetchone()
    con.execute(sql, (escape_string(str(scout_id)), escape_string(
        str(scouting_troop_id)), escape_string(str(datetime.now()))))
    conn.commit()
    if notify:
        flash("{} {} dołącza do \"{}\" w {}".format(
            scout['first_name'], scout['last_name'], scouting_troop['name'], scout_team['name']), 'success')
    con.close()
    conn.close()


def scouting_troop_create(name, scout_team_id, notify=True):
    con, conn = connection()
    sql = "INSERT INTO scouting_troop (name, scout_team_id) VALUES (%s, %s)"
    con.execute("SELECT name FROM scout_team WHERE id_scout_team = %s",
                escape_string(str(scout_team_id)))
    scout_team = con.fetchone()
    con.execute(sql, (escape_string(name), escape_string(str(scout_team_id))))
    conn.commit()
    if notify:
        flash("Stworzono \"{}\" w {}".format(name, scout_team['name']), 'success')
    scouting_troop_id = con.lastrowid
    con.close()
    conn.close()
    return scouting_troop_id
