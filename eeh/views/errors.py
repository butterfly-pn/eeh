from main import APP
from flask import render_template

@APP.errorhandler(404)
def errorhandler404(e):
    return render_template('404.html'), 404