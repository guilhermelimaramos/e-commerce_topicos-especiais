from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
app = Flask(__name__)
login_manager = LoginManager()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = 'dc151bb9f81b92dca919b698'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view = "page_signin"
login_manager.login_message = "Please, Sign-in to continue"
login_manager.login_message_category = "info"

from commerce import routes
