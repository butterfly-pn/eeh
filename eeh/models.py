"""Database tables models"""
from flask_login._compat import unicode
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean, Date, Text
from passlib.hash import sha256_crypt
from main import LM
from dbconnect import connection
from pymysql import escape_string
from collections.abc import Mapping
import gc


@LM.user_loader
def user_load(user_id):
    try:
        con, conn = connection()
        con.execute("SELECT * FROM user WHERE id_user = (%s)",
                    escape_string(str(user_id)))
        user_dict = con.fetchone()
        user = User()
        user.update(user_dict)
        con.close()
        conn.close()
        gc.collect()
        return user
    except:
        return None


class User(dict):

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))

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
