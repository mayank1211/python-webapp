from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from web_application import routes

# Loads in the environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)