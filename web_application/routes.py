from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
# Import login and authentication modules
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from sqlalchemy import create_engine, select, insert, update, delete
# Manual
from web_application import app, db
from web_application.models import Users, Skills, Comments

# Password hashing.
import os
import bcrypt

@app.route("/login", methods=["GET", "POST"])
def login():
    errorMessage = ""
    if request.method == "POST":
        userEmailInput = request.form.get("email")
        
        if not db.session.query(Users).filter_by(Email=userEmailInput).first():
            errorMessage = "User does not exist, please register the user first."
        else:
            userFound = db.session.query(Users).filter_by(Email=userEmailInput).first()
            # Comparing the hashed password due to bcrypt.checkpw not working as expected.
            hashedUserInputPassword = bcrypt.hashpw(request.form.get("password"), userFound.Password)
            if (userFound.Password == hashedUserInputPassword):
                login_user(userFound, True)
                return redirect(url_for('.index'))
            else:
                errorMessage = "Incorrect details, please check and try again later"

    return render_template("login.html", title="Login", errorMessage=errorMessage)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".index"))

    if request.method == "POST":
        userEmailInput = request.form.get("email")
        if db.session.query(Users).filter_by(Email=userEmailInput).first():
            # Redirect the useer to login page with a message stating they are already a member
            userExists = True
        else:
            # Create the standard user
            userExists = False
            db.create_all()
            hashedUserPassword = bcrypt.hashpw(request.form.get("password"), bcrypt.gensalt(12))
            newUser = Users(
                Name = request.form.get("full_name"),
                Email = request.form.get("email_address"),
                Password = hashedUserPassword,
                Role = request.form.get("role"),
                CurrentTeam = request.form.get("current_team"),
            )
            db.session.add(newUser)
            db.session.commit()
        # Redirect the user to login page to sign with their details
        return redirect(url_for(".login", userExists=userExists))
    # Render the register form page on the GET request
    return render_template("register.html", title="Register")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))
    
# Half Complete
@app.route("/")
@app.route("/index")
@login_required
def index():
    users = db.session.query(Users).all()
    skills = db.session.query(Skills).all()
    return render_template("index.html", title="Skills Finder", users=users, skills=skills)

@app.route("/manage/account", methods=["GET"])
@login_required
def manage_account():
    return render_template("manage_account.html", title="Manage Your Profile")

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
        return render_template("update_skill.html", title="Update User's Profile", userId=userId)

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

