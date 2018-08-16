from flask import render_template
from main import APP


@APP.route('/', methods=["GET"])
def home():
    return render_template('home.html')
