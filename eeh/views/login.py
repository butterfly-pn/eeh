from flask import request, redirect, flash, url_for, session
from eeh.view_manager.templating import render_template
from flask_login import current_user, login_user, logout_user
from passlib.handlers.sha2_crypt import sha256_crypt
from main import APP, MAIL
from eeh.models import User
from dbconnect import connection
from pymysql import escape_string
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
import re
import gc
import config

APP.secret_key = "sekret"

ts = URLSafeTimedSerializer(APP.secret_key)

@APP.route('/login/', methods=["GET", "POST"])
def login():
    try:
        if current_user.is_authenticated:
            flash('Już jesteś zalogowany!', 'warning')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
        if request.method == "POST":
            con, conn = connection()
            con.execute("SELECT * FROM user WHERE email = (%s) OR login = %s",
                        (escape_string(request.form['email']), escape_string(request.form['email'])))
            user_dict = con.fetchone()
            user = User()
            user.update(user_dict)
            con.close()
            conn.close()
            gc.collect()
            if user and sha256_crypt.verify(request.form['password'], user['password']):
                con, conn = connection()
                con.execute("SELECT id_scout_team FROM scout_team WHERE scoutmaster_user_id = %s", escape_string(str(user['id_user'])))
                scout_team = con.fetchone()
                con.close()
                conn.close()
                remember_me = request.form['remember-me'] if 'remember_me' in request.form else False
                login_user(user, remember=remember_me)
                session['id_scout_team'] = scout_team['id_scout_team']
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/app/')
            return render_template('login.html', form=request.form, wrong=True)
        return render_template('login.html')
    except Exception as error:
        flash('Błąd: ' + str(error), 'danger')
        return redirect('/')


def send_confirmation_email(mail):
    with MAIL.connect() as conn:
        print(mail)
        token = ts.dumps(mail, salt='email-confirm-key')
        print(token)
        msg = Message("EEH - Potwierdź swój adres email",
                    sender=config.MAIL_USERNAME, recipients=[mail])
        msg.html = render_template('verify_email.html', token=token)
        conn.send(msg)

@APP.route('/register/', methods=["GET", "POST"])
def register():
    next_url = request.args.get('next')
    if not current_user.is_authenticated:
        try:
            if request.method == "POST":
                con, conn = connection()
                form = request.form
                email = form['email']
                password = sha256_crypt.encrypt((str(form['password'])))
                used_username = con.execute("SELECT * FROM user WHERE login = (%s)", escape_string(request.form['login']))
                if "@" not in email:
                    wrong_email = True
                else:
                    wrong_email = False
                if used_username or wrong_email:
                    return render_template('register.html', form=form, used_username=used_username, wrong_email=wrong_email)
                con.execute("INSERT INTO scout (first_name, last_name) VALUES (%s, %s)", (escape_string(form['first-name']), escape_string(form['last-name'])))
                conn.commit()
                scout_id = con.lastrowid
                sql = "INSERT INTO user (login, password, email, scout_id) VALUES (%s, %s, %s, " + str(
                    scout_id) + ")"
                con.execute(sql, (escape_string(form['login']), escape_string(password), escape_string(form['email'])))
                conn.commit()
                flash("Zarejestrowano pomyślnie!", 'success')
                send_confirmation_email(form['email'])
                con.close()
                conn.close()
                gc.collect()
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

@APP.route('/user/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
        con, conn = connection()
        user = con.execute("UPDATE user SET email_confirm = 1 WHERE email = (%s)", escape_string(email))
        conn.commit()
        flash("Adres email zweryfikowany!", 'success')
        con.close()
        conn.close()
        gc.collect()
    except Exception as error:
        flash("Blad" + str(error), 'danger')
    return redirect('/')
