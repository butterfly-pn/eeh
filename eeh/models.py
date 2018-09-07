"""Database tables models"""
from flask_login._compat import unicode
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean, Date, Text
from passlib.hash import sha256_crypt
from main import DB, LM
from dbconnect import connection
from pymysql import escape_string
import gc


@LM.user_loader
def user_load(user_id):
    con, conn = connection()
    con.execute("SELECT * FROM user WHERE id = (%s)", escape_string=user_id)
    user = con.fetchone()
    con.close()
    conn.close()
    gc.collect()
    return user


class Druzyna(DB.Model):
    """
    User model for reviewers.
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    name = Column(String(20), unique=True)
    email = Column(String(200), unique=True)
    confirm_mail = Column(Boolean, default=False)
    password = Column(String(200), default='')
    current_plan = Column(Integer)
    admin = Column(Boolean, default=False)
    ban = Column(Boolean, default=False)

    def check_password(self, password):
        if sha256_crypt.verify(password, self.password):
            return True

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Harcerz(DB.Model):
    """Model for records"""
    __tablename__ = "harcerz"
    id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(200))
    second_name = Column(String(200))
    last_name = Column(String(200))
    birthdate = Column(Date)
    pesel = Column(Integer)
    adres = Column(String(200))
    nrkont = Column(String(13))
    funkcja = Column(Integer)
    druzyna = Column(Integer)

class HarcerzPlan(DB.Model):
    """Model for work plan with scout"""
    __tablename__ = "harcerzplan"
    id = Column(Integer, autoincrement=True, primary_key=True)
    plan_id = Column(Integer)
    harcerz_id = Column(Integer)
    charakterystyka = Column(Text)
    cele = Column(Text)

class Plan(DB.Model):
    """Model for work plan"""
    __tablename__ = "plan"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(200))
    typ = Column(String(30))
    druzyna_id = Column(Integer)
    wizja = Column(Text)
    cele = Column(Text)
    zz = Column(Text)
