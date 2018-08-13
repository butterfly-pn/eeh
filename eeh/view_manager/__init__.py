from flask_login import current_user
from flask import flash, request, redirect, url_for
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            print("nie zalogowano")
            flash("Musisz być zalogowany", 'warning')
            next_url = request.url
            return redirect(url_for('login', next=next_url))
        return func(*args, **kwargs)
    return wrap
