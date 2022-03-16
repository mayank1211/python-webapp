import os
from flask import Flask, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.secret_key = os.environ.get("SECRET_KEY")
# Initialize SQLAlchemy connection with the database
db = SQLAlchemy(app)

# Initialize flask login manager to authentication and sessions expiry
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.refresh_view = 'relogin'
login_manager.needs_refresh_message = (
    u"Session timedout, please re-login to access the application")
login_manager.needs_refresh_message_category = "info"

# Function to redirect the user to login page if not already logged in.
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

# Import routes and create_database_and_data function from create_data.py to create tables and users.
import routes
from create_data import create_database_and_data
# Delete/Drop existing table and re-create the tables with fresh temp data.
with app.app_context():
    # db.create_all()
    create_database_and_data()
