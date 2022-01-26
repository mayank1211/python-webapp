# http://pycrud-app.herokuapp.com/account

import os
from dotenv import load_dotenv
from flask import Flask
# Import modules required to perform sqLite commands to create and fetch existing data from the sqlite flaskApp.db files
from sqlalchemy import create_engine, select, insert, update, delete
# from forms import RegistrationForm
# from flask_login import *
from models.models import *

# Secrets config. Move it later to config.py file!
load_dotenv()
app = Flask(__name__)

# Password hashing.
import bcrypt
bcrypt.hashpw(os.getenv('Hashing_Password'), bcrypt.gensalt( 12 ))


# Create a connection with the local sqlite database file.
engine = create_engine('sqlite:///flaskApp.db', echo=False)
# Check and create new tables with defined schema from Models/model.py file
metadata.create_all(engine, checkfirst=True)

# def do_insert():
#     stmt = insert(users).values(
#         Name='nathan', 
#         Email='Arnold', 
#         Password='2000-01-31',
#         Role='2000-01-31',
#         CurrentTeam='2000-01-31')
    
#     with engine.begin() as con:
#         result = con.execute(stmt)
#         x = result.inserted_primary_key['Id']
#     return result.inserted_primary_key['Id']

# def do_insert_skill(userId):
#     stmt = insert(skills).values(
#         UserId=userId,
#         SkillName='SkillName', 
#         SkillRating=1)
    
#     with engine.begin() as con:
#         result = con.execute(stmt)
#     return result.inserted_primary_key['Id']

# def do_insert_comment(userId):
#     stmt = insert(comments).values(
#         UserId=userId,
#         Comments='Id qui enim ipsum sit laboris reprehenderit ex dolore ullamco tempor consequat aliqua. Sint ut amet amet et laborum fugiat culpa cillum minim. Mollit dolor labore pariatur commodo laborum eiusmod ex. Veniam Lorem tempor sunt deserunt mollit non cillum commodo laboris do voluptate in. Qui officia eiusmod ut culpa eiusmod laborum sint officia esse dolor.')
    
#     with engine.begin() as con:
#         result = con.execute(stmt)
#     return result.inserted_primary_key['Id']

# createdUser=do_insert()
# do_insert_skill(createdUser)
# do_insert_comment(createdUser)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        def get_hashed_password(plain_text_password):
            # Hash a password for the first time
            #   (Using bcrypt, the salt is saved into the hash itself)
            return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

        def check_password(plain_text_password, hashed_password):
            # Check hashed password. Using bcrypt, the salt is saved into the hash itself
            return bcrypt.checkpw(plain_text_password, hashed_password)

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
