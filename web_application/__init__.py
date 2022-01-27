from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

# Loads in the environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import web_application.routes
from web_application.models import Users