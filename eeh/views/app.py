from flask import render_template, redirect, flash
from flask_login import current_user
from main import APP
from dbconnect import connection


@APP.route('/app/')
def app():
    con, conn = connection()
    sql = "SELECT * FROM scout_team WHERE scout_master_user_id = "
    if current_user.is_authenticated:
        harcerze = Harcerz.query.filter_by(druzyna=current_user['id']).all()
    else:
        flash("Zaloguj się", "warning")
        return redirect('/')
    return render_template('app.html', harcerze=harcerze)
