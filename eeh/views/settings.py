from flask import render_template, session, request, redirect
from flask_login import current_user
from main import APP
from eeh.view_manager import komenda_required
from dbconnect import connection
from pymysql import escape_string


@APP.route('/settings/', methods=['GET'])
@komenda_required
def settings_get():
    con, conn = connection()
    con.execute("SELECT * FROM scout_team WHERE id_scout_team = %s", escape_string(str(session['id_scout_team'])))
    scout_team = con.fetchone()
    con.close()
    conn.close()
    return render_template('settings.html', scout_team=scout_team)

@APP.route('/settings/', methods=['POST'])
@komenda_required
def settings_post():
    con, conn = connection()
    con.execute("SELECT * FROM scout_team WHERE id_scout_team = %s", escape_string(str(session['id_scout_team'])))
    current_team = con.fetchone()
    if request.form['email'] != current_user['email']:
        con.execute("UPDATE user SET email = %s, email_confirm = 0 WHERE id_user = %s", (escape_string(request.form['email']), escape_string(str(current_user['id_user']))))
        conn.commit()
    if request.form['name'] != current_team['name']:
        con.execute("UPDATE scout_team SET name = %s WHERE id_scout_team = %s", (escape_string(request.form['name']), escape_string(str(session['id_scout_team']))))
        conn.commit()
    con.close()
    conn.close()
    return redirect('/settings/')
