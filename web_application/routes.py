import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session
# Import login and authentication modules
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from sqlalchemy import create_engine, select, insert, update, delete
# Password hashing.
from passlib.hash import sha256_crypt
# Import flask app and databaase config from run.py
from run import app, db
# Import all database models from models.py file to create and interact with data.
from models import Users, Skills, Comments


def find_user_with_email(email):
    return db.session.query(Users).filter_by(email=email).first()


def save_data(*args):
    # Check if the any data parameter is passed.
    if args:
        for ar in args:
            # If passed then add the data to db sessions before committing.
            db.session.add(ar)
    db.session.commit()


@app.route("/login", methods=["GET", "POST"])
def login():
    errorMessage = ""
    if request.method == "POST":
        # Check if the input email address matches any users email storeed in database, if not show error message to the user
        if not find_user_with_email(request.form.get("email_address")):
            errorMessage = "User does not exist, please register the user first."
        else:
            # If matching email is found try sign in the user, if both email address and password match.
            userFound = find_user_with_email(request.form.get("email_address"))
            # Comparing the hashed password with hashed input.
            if sha256_crypt.verify(request.form.get("password"), userFound.password):
                login_user(userFound)
                session.modified = True
                app.permanent_session_lifetime = timedelta(minutes=1)
                return redirect(url_for('.index'))
            else:
                errorMessage = "Incorrect details, please check and try again later"
            print()
    return render_template("login.html", title="Sign in", errorMessage=errorMessage)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".index"))

    errorMessage = ""
    if request.method == "POST":
        if find_user_with_email(request.form.get("email_address")):
            errorMessage = "Email entered alread exists."
        else:
            # Create the standard user
            newUser = Users(
                name=request.form.get("full_name"),
                email=request.form.get("email_address"),
                password=sha256_crypt.encrypt(request.form.get("password")),
                jobRole=request.form.get("role"),
                currentTeam=request.form.get("current_team"),
            )
            save_data(newUser)
            # Redirect the user to login page to sign with their details
            return redirect(url_for(".login"))
    # Render the register form page on the GET request
    return render_template("register.html", title="Register", errorMessage=errorMessage)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('.login'))


@app.route("/")
@app.route("/index")
@login_required
def index():
    users = db.session.query(Users).all()
    skills = db.session.query(Skills).all()
    return render_template("index.html", title="Skills Finder", users=users, skills=skills)


@app.route("/my/account/<userId>", methods=["GET"])
@login_required
def my_account(userId):
    user = db.session.query(Users).filter_by(id=userId).first()
    return render_template("my_account.html", title="Manage Your Profile", user=user)


@app.route("/update/account/<userId>", methods=["GET", "POST"])
@login_required
def update_account(userId):
    user = db.session.query(Users).filter_by(id=userId).first()
    if request.method == "POST":
        user.name = request.form.get("full_name")
        user.email = request.form.get("email_address")
        user.jobRole = request.form.get("role")
        user.currentTeam = request.form.get("current_team")
        user.lastUpdatedAt = datetime.utcnow()

        if request.form.get("password"):
            user.password = sha256_crypt.encrypt(request.form.get("password"))

        save_data()
        return redirect(url_for(".my_account", userId=userId))
    return render_template("update_my_profile.html", title="Update Your Profile", user=user)


@app.route("/delete/account/<userId>", methods=["GET"])
@login_required
def delete_profile(userId):
    if int(userId) == current_user.id or current_user.userRole == "Admin":
        db.session.query(Users).filter_by(id=userId).delete()
        db.session.query(Skills).filter_by(userId=userId).delete()
        db.session.query(Comments).filter_by(userId=userId).delete()
        save_data()
    return redirect(url_for(".index"))


@app.route("/manage/accounts", methods=["GET"])
@login_required
def manage_accounts():
    if current_user.userRole != "Admin":
        return redirect(url_for('.index'))

    users = db.session.query(Users).all()
    return render_template("manage_accounts.html", title="Manage Profile's", users=users)


@app.route("/make/admin/<userId>", methods=["GET"])
@login_required
def make_admin(userId):
    if current_user.userRole != "Admin":
        return redirect(url_for('.index'))

    user = db.session.query(Users).filter_by(id=userId).first()
    user.userRole = "Admin"
    user.lastUpdatedAt = datetime.utcnow()
    save_data()
    return redirect(url_for(".manage_accounts", userId=userId))


@app.route("/remove/admin/<userId>", methods=["GET"])
@login_required
def remove_admin(userId):
    if current_user.userRole != "Admin":
        return redirect(url_for('.index'))

    # check if more than 1 admin exists if not then redirect user to manage_accounts page without any chances
    if (len(db.session.query(Users).filter_by(userRole="Admin").all()) > 1):
        user = db.session.query(Users).filter_by(id=userId).first()
        user.userRole = "Standard"
        user.lastUpdatedAt = datetime.utcnow()
        save_data()
    return redirect(url_for(".manage_accounts"))


@app.route("/profile/<userId>", methods=["GET"])
@login_required
def profile(userId):
    user = db.session.query(Users).filter_by(id=userId).first()
    skills = db.session.query(Skills).filter_by(userId=userId).all()
    comment = db.session.query(Comments).filter_by(userId=userId).first()
    return render_template("profile.html", title="User's profile", user=user, skills=skills, comment=comment)


@app.route("/add_skill/<userId>", methods=["GET", "POST"])
@login_required
def add_skill(userId):
    if request.method == "POST":
        skill = Skills(
            userId=userId,
            skillName=request.form.get("new_skill_name"),
            skillRating=request.form.get("new_skill_rating")
        )
        db.session.query(Users).filter_by(id=userId).update({'lastUpdatedAt': datetime.utcnow()})
        save_data(skill)
        return redirect(url_for(".profile", userId=userId))
    else:
        return render_template("add_skill.html", title="Update User's Profile", userId=userId)


@app.route("/delete_skill/<userId>/<skillId>", methods=["GET"])
@login_required
def delete_skill(userId, skillId):
    db.session.query(Skills).filter_by(id=skillId).delete()
    db.session.query(Users).filter_by(id=userId).update({'lastUpdatedAt': datetime.utcnow()})
    save_data()
    return redirect(url_for(".profile", userId=userId))


@app.route("/update_comment/<userId>", methods=["GET", "POST"])
@login_required
def update_comment(userId):
    if request.method == "POST":
        if not db.session.query(Comments).filter_by(userId=userId).first():
            comment = Comments(
                userId=userId,
                comments=request.form.get("comment")
            )
            db.session.add(comment)
        else:
            if request.form.get("comment"):
                userComment = db.session.query(
                    Comments).filter_by(userId=userId).first()
                userComment.comments = request.form.get("comment")
            else:
                db.session.query(Comments).filter_by(userId=userId).delete()
        db.session.query(Users).filter_by(id=userId).update({'lastUpdatedAt': datetime.utcnow()})
        save_data()
        return redirect(url_for(".profile", userId=userId))
    else:
        currentComment = db.session.query(
            Comments).filter_by(userId=userId).first()
        return render_template("update_comment.html", title="Update User's Comments", userId=userId, currentComment=currentComment)


@app.route("/delete_comment/<userId>", methods=["GET"])
@login_required
def delete_comment(userId):
    db.session.query(Comments).filter_by(userId=userId).delete()
    db.session.query(Users).filter_by(id=userId).update({'lastUpdatedAt': datetime.utcnow()})
    save_data()
    return redirect(url_for(".profile", userId=userId))
