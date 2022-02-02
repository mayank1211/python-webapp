import os
from dotenv import load_dotenv
from flask import Flask, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager
# Flask log monitoring
import flask_monitoringdashboard as dashboard

# Loads in the environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS")
app.secret_key = os.environ.get("SECRET_KEY")
# Initialize SQLAlchemy connection with sqlite database locally
db = SQLAlchemy(app)
# Initialize flask monitoring for debugging and analystics
dashboard.config.init_from(file='/config.cfg')
dashboard.bind(app)

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


# Import routes and create_database_and_data function from models.py to create tables and users.
import routes
from models import create_database_and_data
# Call function from models.py file to required create tables and users
create_database_and_data()
