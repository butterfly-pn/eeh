from flask import render_template, request, redirect, flash
from flask_login import current_user
from main import APP
from datetime import datetime
from eeh.view_manager import login_required
from dbconnect import connection
from pymysql import escape_string

def valid_pesel(pesel):
    if type(pesel) == str and len(pesel) == 11:
        return True
    return False

@APP.route('/add/', methods=["POST", "GET"])
@login_required
def add_get():
    if request.method == "GET":
        return render_template('add.html')
    elif request.method == "POST":
        try:
            con, conn = connection()
            if not valid_pesel(request.form['pesel']):
                flash("Zły pesel", 'warning')
                return redirect('/add/')
            sql = "INSERT INTO scout (first_name, middle_name, last_name, birthdate, pesel, address, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            print(sql)
            con.execute(sql, (escape_string(request.form['first-name']), escape_string(request.form['middle-name']), escape_string(request.form['last-name']), escape_string(str(request.form['birthdate'])), escape_string(request.form['pesel']), escape_string(request.form['address']), escape_string(request.form['phone'])))
            conn.commit()
            con.close()
            conn.close()
            flash("Success!", 'success')
        except Exception as error:
            flash("Error: " + str(error), 'danger')
        return redirect('/')
