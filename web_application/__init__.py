import os
from dotenv import load_dotenv
from flask import Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager
# Flask log monitoring
import flask_monitoringdashboard as dashboard

# Loads in the environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
app.secret_key = os.environ.get("SECRET_KEY")
db = SQLAlchemy(app)
dashboard.config.init_from(file='/config.cfg')
dashboard.bind(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
# Function to redirect the user to login page if not already logged in.
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

import web_application.routes
from web_application.models import create_database_and_data

create_database_and_data()