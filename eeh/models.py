"""Database tables models"""
from flask_login._compat import unicode
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean, Date, Text
from passlib.hash import sha256_crypt
from main import DB, LM
from dbconnect import connection
from pymysql import escape_string
import gc


class User(dict):
    """
    User model for reviewers.
    """
    def check_password(self, password):
        if sha256_crypt.verify(password, self['password']):
            return True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self['id'])

    def __repr__(self):
        return '<User %r>' % (self['name'])


@LM.user_loader
def user_load(user_id):
    con, conn = connection()
    con.execute("SELECT * FROM user WHERE id = (%s)",
                escape_string(str(user_id)))
    user = con.fetchone()
    user = User()
    con.close()
    conn.close()
    gc.collect()
    return user

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
