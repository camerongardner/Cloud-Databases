# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions necessary to work with the SQL database and users
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'main.login'  # Updated to include Blueprint prefix
