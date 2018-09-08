"""Main file of the application"""

from flask_login import LoginManager
from flask_mail import Mail
from eeh import create_app
import config


APP = create_app(mail_server=config.MAIL_SERVER, mail_port=config.MAIL_PORT, mail_use_ssl=config.MAIL_USE_SSL, mail_username=config.MAIL_USERNAME,
                 mail_password=config.MAIL_PASSWORD)
LM = LoginManager()
LM.init_app(APP)
LM.login_view = 'login'
MAIL = Mail(APP)
APP.config['JSON_SORT_KEYS'] = False
