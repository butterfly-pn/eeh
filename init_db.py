"""Create daatabase"""

from sqlalchemy import create_engine
from main import DB
from eeh import models
from passlib.hash import sha256_crypt


def db_start():
    engine = create_engine('sqlite:///tmp/test.db', convert_unicode=True)
    DB.create_all()
    DB.session.commit()

    user = models.Druzyna(name='7pdh', password=sha256_crypt.encrypt("h@sl0"), email='pniedzwiedzinski19@gmail.com')
    user.confirm_mail = True
    user.admin = True
    DB.session.add(user)
    DB.session.commit()


if __name__ == '__main__':
    db_start()
