from flask import render_template, request, redirect, flash
from flask_login import current_user
from main import APP, DB
from eeh.models import Harcerz
from datetime import datetime
from eeh.view_manager import login_required

@APP.route('/delete/<identifier>/', methods=['GET'])
@login_required
def delete(identifier):
    harcerz = Harcerz.query.filter_by(id=identifier).first()
    if harcerz.druzyna == current_user.id:
        DB.session.delete(harcerz)
        DB.session.commit()
    else:
        flash("Nie mozesz tego zrobic", 'warning')
    return redirect('/')
