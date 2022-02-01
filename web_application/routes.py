import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
# Import login and authentication modules
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from sqlalchemy import create_engine, select, insert, update, delete
# Password hashing.
import bcrypt
# Manual
from web_application import app, db
from web_application.models import Users, Skills, Comments

# Complete
@app.route("/login", methods=["GET", "POST"])
def login():
    errorMessage = ""
    if request.method == "POST":
        # Check if the input email address matches any users email storeed in database, if not show error message to the user
        if not db.session.query(Users).filter_by(Email=request.form.get("email")).first():
            errorMessage = "User does not exist, please register the user first."
        else:
            # if matching email if found try sign in the user only if both email address and password matches.
            userFound = db.session.query(Users).filter_by(Email=request.form.get("email")).first()
            # Comparing the hashed password due to bcrypt.checkpw not working as expected.
            if (userFound.Password == bcrypt.hashpw(request.form.get("password"), userFound.Password)):
                login_user(userFound, True)
                session.permanent = True
                return redirect(url_for('.index'))
            else:
                errorMessage = "Incorrect details, please check and try again later"
    return render_template("login.html", title="Login", errorMessage=errorMessage)

# Complete
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".index"))

    errorMessage=""
    if request.method == "POST":
        if db.session.query(Users).filter_by(Email=request.form.get("email_address")).first():
            errorMessage="Email entered alread exists."
        else:
            # Create the standard user
            newUser = Users(
                Name = request.form.get("full_name"),
                Email = request.form.get("email_address"),
                Password = bcrypt.hashpw(request.form.get("password"), bcrypt.gensalt(12)),
                JobRole = request.form.get("role"),
                CurrentTeam = request.form.get("current_team"),
            )
            db.session.add(newUser)
            db.session.commit()
            # Redirect the user to login page to sign with their details
            return redirect(url_for(".login"))
    # Render the register form page on the GET request
    return render_template("register.html", title="Register", errorMessage=errorMessage)

# Complete
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

# Complete
@app.route("/")
@app.route("/index")
@login_required
def index():
    users = db.session.query(Users).all()
    skills = db.session.query(Skills).all()
    return render_template("index.html", title="Skills Finder", users=users, skills=skills)

# Complete
@app.route("/my/account/<userId>", methods=["GET"])
@login_required
def my_account(userId):
    user = db.session.query(Users).filter_by(Id=userId).first()
    return render_template("my_account.html", title="Manage Your Profile", user=user)

# Complete
@app.route("/update/account/<userId>", methods=["GET", "POST"])
@login_required
def update_account(userId):
    user = db.session.query(Users).filter_by(Id=userId).first()
    if request.method == "POST":
        user.Name = request.form.get("full_name")
        user.Email = request.form.get("email_address")
        user.JobRole = request.form.get("role")
        user.CurrentTeam = request.form.get("current_team")

        if request.form.get("password"):
            hashedUserPassword = bcrypt.hashpw(request.form.get("password"), bcrypt.gensalt(12))
            user.Password = hashedUserPassword

        db.session.commit()
        return redirect(url_for(".my_account", userId=userId))
    return render_template("update_my_profile.html", title="Update Your Profile", user=user)

# Complete - (Redirect based on url coming from)
@app.route("/delete/account/<userId>", methods=["GET"])
@login_required
def delete_profile(userId):
    if userId == current_user.Id or current_user.UserRole == "Admin":
        db.session.query(Users).filter_by(Id=userId).delete()
        db.session.query(Skills).filter_by(UserId=userId).delete()
        db.session.query(Comments).filter_by(UserId=userId).delete()
        db.session.commit()
    return redirect(url_for(".index"))

# Complete
@app.route("/manage/accounts", methods=["GET"])
@login_required
def manage_accounts():
    if current_user.UserRole != "Admin":
        return redirect(url_for('.index'))

    users = db.session.query(Users).all()
    return render_template("manage_accounts.html", title="Manage Profile's", users=users)

# Complete
@app.route("/make/admin/<userId>", methods=["GET"])
@login_required
def make_admin(userId):
    if current_user.UserRole != "Admin":
        return redirect(url_for('.index'))

    user = db.session.query(Users).filter_by(Id=userId).first()
    user.UserRole = "Admin"
    db.session.commit()
    return redirect(url_for(".manage_accounts", userId=userId))

# Complete
@app.route("/remove/admin/<userId>", methods=["GET"])
@login_required
def remove_admin(userId):
    if current_user.UserRole != "Admin":
        return redirect(url_for('.index'))

    print('ashdgjahsgdjasgd ', len(db.session.query(Users).filter_by(UserRole="Admin").all()))

    # check if more than 1 admin exists if not then redirect user to manage_accounts page without any chances
    if (len(db.session.query(Users).filter_by(UserRole="Admin").all()) > 1):
        user = db.session.query(Users).filter_by(Id=userId).first()
        user.UserRole = "Standard"
        db.session.commit()
    return redirect(url_for(".manage_accounts"))

# Complete
@app.route("/profile/<userId>", methods=["GET"])
@login_required
def profile(userId):
    user = db.session.query(Users).filter_by(Id=userId).first()
    skills = db.session.query(Skills).filter_by(UserId=userId).all()
    comment = db.session.query(Comments).filter_by(UserId=userId).first()
    return render_template("profile.html", title="User's profile", user=user, skills=skills, comment=comment)

# Complete
@app.route("/add_skill/<userId>", methods=["GET", "POST"])
@login_required
def add_skill(userId):
    if request.method == "POST":
        skill = Skills(
            UserId = userId, 
            SkillName = request.form.get("new_skill_name"),
            SkillRating = request.form.get("new_skill_rating")
        )
        db.session.add(skill)
        db.session.commit()
        return redirect(url_for(".profile", userId=userId))
    else:
        return render_template("add_skill.html", title="Update User's Profile", userId=userId)

# Complete
@app.route("/delete_skill/<userId>/<skillId>", methods=["GET"])
@login_required
def delete_skill(userId, skillId):
    db.session.query(Skills).filter_by(Id=skillId).delete()
    db.session.commit()
    return redirect(url_for(".profile", userId=userId))

# Complete (Adding and Updating existing comments)
@app.route("/update_comment/<userId>", methods=["GET", "POST"])
@login_required
def update_comment(userId):
    if request.method == "POST":
        if not db.session.query(Comments).filter_by(UserId=userId).first():
            comment = Comments(
                UserId = userId, 
                Comments = request.form.get("comment")
            )
            db.session.add(comment)
        else:
            if request.form.get("comment"):
                userComment = db.session.query(Comments).filter_by(UserId=userId).first()
                userComment.Comments = request.form.get("comment")
            else:
                db.session.query(Comments).filter_by(UserId=userId).delete()

        db.session.commit()
        return redirect(url_for(".profile", userId=userId))
    else:
        currentComment = db.session.query(Comments).filter_by(UserId=userId).first()
        return render_template("update_comment.html", title="Update User's Comments", userId=userId, currentComment=currentComment)

# Complete
@app.route("/delete_comment/<userId>", methods=["GET"])
@login_required
def delete_comment(userId):
    db.session.query(Comments).filter_by(UserId=userId).delete()
    db.session.commit()
    return redirect(url_for(".profile", userId=userId))

