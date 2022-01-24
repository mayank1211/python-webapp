# http://pycrud-app.herokuapp.com/account

# Import the following the components from flask_login package (current_user, login_required, login_user, logout_user)
# from flask_login import *
# Import all the modules and features offered by flask
from multiprocessing.connection import wait
import os
from time import sleep
from flask import *
from forms import RegistrationForm

app = Flask(__name__)

# Secrets config. Move it later to config.py file!
from dotenv import load_dotenv
load_dotenv()

# SECRET_KEY = os.urandom(32)
SECRET_KEY = environ.get('SECRET_KEY')
FLASK_APP = environ.get('FLASK_APP')
FLASK_ENV = environ.get('FLASK_ENV')

# Database
SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_ECHO = environ.get("SQLALCHEMY_ECHO")
SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")



@app.route("/login")
def login():
    return render_template("login.html", title="Login")


@app.route("/register")
def sign_up():
    Regform = RegistrationForm()
    return render_template("register.html", title="Register", form=Regform)


@app.route("/")
def index():
    return render_template("index.html", title="Skills Finder")


@app.route("/profile/<username>", methods=["GET"])
def profile(username):
    username = username
    return render_template("profile.html", title="User's profile", username=username)


@app.route("/delete_skill/<username>", methods=["GET"])
def delete_skill(username):
    return redirect(url_for(".profile", username=username))


@app.route("/update_skill/<username>", methods=["GET", "POST"])
def update_skill(username):
    if request.method == "POST":
        # Should be the name of the user logged in
        return render_template(
            "update_skill.html", title="Update User's Profile", username=username
        )
    else:
        return render_template(
            "update_skill.html", title="Update User's Profile", username=username
        )


@app.route("/update_comment/<username>", methods=["GET", "POST"])
def update_comment(username):
    username = username
    if request.method == "POST":
        # Should be the name of the user logged in
        return render_template(
            "update_comment.html", title="Update User's Profile", username=username
        )
    else:
        return render_template(
            "update_comment.html", title="Update User's Profile", username=username
        )


@app.route("/manage/account", methods=["GET"])
def manage_account():
    return render_template("manage_account.html", title="Manage Your Profile")
