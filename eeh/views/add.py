from flask import render_template, request, redirect, flash
from flask_login import current_user
from main import APP
from datetime import datetime
from eeh.view_manager import login_required


@APP.route('/add/', methods=["POST", "GET"])
@login_required
def add_get():
    if request.method == "GET":
        return render_template('add.html')
    elif request.method == "POST":
        try:
            new = Harcerz()
            new.first_name = request.form['first-name']
            new.second_name = request.form['second-name']
            new.last_name = request.form['last-name']
            new.birthdate = datetime.strptime(request.form['birthdate'], '%d-%m-%Y')
            new.pesel = request.form['pesel']
            new.adres = request.form['adres']
            new.nrkont = request.form['nrkont']
            new.funkcja = request.form['funkcja']
            new.druzyna = current_user['id']
            DB.session.add(new)
            DB.session.commit()
            flash("Success!", 'success')
        except Exception as error:
            flash("Error: " + error, 'danger')
        return redirect('/')
