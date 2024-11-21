# app.py

from flask import Flask
from config import Config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Import and initialize extensions
from extensions import db, login
db.init_app(app)
login.init_app(app)

# Import models and routes after initializing extensions to avoid circular imports
import models
from routes import main as main_blueprint  # Import the Blueprint

# Register the Blueprint
app.register_blueprint(main_blueprint)

# Run the app if executed directly
if __name__ == '__main__':
    app.run(debug=True)
