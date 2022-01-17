# http://pycrud-app.herokuapp.com/account

# Import the following the components from flask_login package (current_user, login_required, login_user, logout_user)
# from flask_login import *
# Import all the modules and features offered by flask
import os
from flask import *
from forms import RegistrationForm
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/login")
def login():
    return render_template("login.html", title="Login - NHS.UK")


@app.route("/register")
def sign_up():
    Regform = RegistrationForm()
    return render_template("register.html", title="Register - NHS.UK", form=Regform)


@app.route("/")
def index():
    return render_template("index.html", title="Skills Finder - NHS.UK")


@app.route("/update", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        # Should be the name of the user logged in
        return render_template("profile.html", title="Update User's Profile")
    else:
        return render_template("profile.html", title="Update User's Profile")


@app.route("/manage/account", methods=["GET"])
def manage_account():
    return render_template("manage_account.html", title="Manage Your Profile")
