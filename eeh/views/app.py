from flask import render_template
from main import APP

@APP.route('/app/', methods=["GET"])
def app():
    return render_template('app.html')
