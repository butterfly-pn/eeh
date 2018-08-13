from flask import render_template
from flask_login import current_user
from main import APP
from eeh.view_manager import login_required


@APP.route('/settings/')
@login_required
def settings():
    return render_template('settings.html')
