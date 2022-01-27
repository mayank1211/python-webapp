from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, select, insert, update, delete
# Manual
from web_application.__init__ import app, db

# Password hashing.
import os
import bcrypt
bcrypt.hashpw(os.getenv('Hashing_Password'), bcrypt.gensalt( 12 ))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        metadata.bind = engine

        result = users.query(users).filter(users.name=='nathan').first() 
        print(result)
        for row in result:
            print(row.Id)
            # result.close()

#         def get_hashed_password(plain_text_password):
#             # Hash a password for the first time
#             #   (Using bcrypt, the salt is saved into the hash itself)
#             return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

#         def check_password(plain_text_password, hashed_password):
#             # Check hashed password. Using bcrypt, the salt is saved into the hash itself
#             return bcrypt.checkpw(plain_text_password, hashed_password)

    return render_template("login.html", title="Login")



@app.route("/register")
def sign_up():
    Regform = RegistrationForm()
    return render_template("register.html", title="Register", form=Regform)

@app.route("/")
@app.route("/index")
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
