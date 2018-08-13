"""Main file of the application"""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from eeh import create_app


APP = create_app('sqlite:///test.db')
DB = SQLAlchemy()
DB.app = APP
DB.init_app(APP)
LM = LoginManager()
LM.init_app(APP)
LM.login_view = 'login'
MAIL = Mail(APP)
APP.config['JSON_SORT_KEYS'] = False
