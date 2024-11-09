from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)

#xavier
bcrypt = Bcrypt(app)
loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = 'login_'
loginmanager.login_message = 'Please log in to access this page.'

SECURITY_EMAIL_SENDER = 'admin@odlanahor.store'

mail = Mail(app)

app.config.from_object(Config)
mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
