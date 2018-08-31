from flask import request, redirect, render_template, flash, url_for
from flask_login import current_user, login_user, logout_user
from passlib.handlers.sha2_crypt import sha256_crypt
from main import APP, DB
from eeh.models import Druzyna
import re


@APP.route('/login/', methods=["GET", "POST"])
def login():
    try:
        if current_user.is_authenticated:
            flash('Już jesteś zalogowany!', 'warning')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
        if request.method == "POST":
            user = Druzyna.query.filter_by(email=request.form['mail']).first()
            if user and user.check_password(request.form['password']):
                try:
                    print("true")
                    remember = request.form['remember']
                except Exception as error:
                    print(error)
                    remember = False
                login_user(user, remember=remember)
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/app/')
            return render_template('login.html', form=request.form, wrong=True)
        else:
            return render_template('login.html')
    except Exception as error:
        flash('Błąd: ' + str(error), 'danger')
        return redirect('/')


@APP.route('/register/', methods=["GET", "POST"])
def register():
    next_url = request.args.get('next')
    if not current_user.is_authenticated:
        try:
            if request.method == "POST":
                form = request.form
                name = form['full-name']
                email = form['email']
                password = form['password']
                used_name = Druzyna.query.filter_by(name=name).first()
                if used_name:
                    used_name = True
                else:
                    used_name = False
                if "@" not in email:
                    wrong_email = True
                else:
                    wrong_email = False
                if used_name or wrong_email:
                    return render_template('register.html', form=form, used_username=used_name, wrong_email=wrong_email)
                user = Druzyna(name=name, password=password, email=email)
                DB.session.add(user)
                DB.session.commit()
                flash("Zarejestrowano pomyślnie!", 'success')
                return redirect(url_for('login', next=next_url, username=email))
            else:
                return render_template('register.html')
        except Exception as error:
            flash('Błąd: '+str(error), 'danger')
            return redirect('/')
    else:
        flash("Jesteś już zalogowany!", 'warning')
        return redirect(next_url)


@APP.route("/logout/")
# @login_required
def logout():
    try:
        logout_user()
        return redirect('/')
    except Exception as e:
        flash('Błąd: '+str(e), 'danger')
        return redirect('/')

APP.secret_key = "sekret"
