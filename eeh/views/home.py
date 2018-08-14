from flask import render_template, redirect, flash
from flask_login import current_user
from main import APP
from eeh.models import Harcerz

@APP.route('/')
def homepage():
    if current_user.is_authenticated:
        harcerze = Harcerz.query.filter_by(druzyna=current_user.id).all()
    else:
        flash("Zaloguj się", "warning")
        return redirect('/app/')
    return render_template('homepage.html', harcerze=harcerze)
