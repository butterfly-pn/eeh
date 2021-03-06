import os
from flask import Flask


def create_app(mail_server="", mail_port="", mail_use_ssl="", mail_username="",
               mail_password=""):
    app = Flask(__name__)
    app.static_path = os.path.join(os.path.abspath(__file__), 'static')
    app.config.update(
        MAIL_SERVER=mail_server,
        MAIL_PORT=mail_port,
        MAIL_USE_SSL=mail_use_ssl,
        MAIL_USERNAME=mail_username,
        MAIL_PASSWORD=mail_password
    )
    return app
