from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cce8ad6ed66fdcf1fc708054044f02c6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# ORM
db = SQLAlchemy(app)

# Encrypt passwords
bcrypt = Bcrypt(app)

# Login Manager
login_manager = LoginManager(app)

# Set a login view
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
