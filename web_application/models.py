import datetime
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy import inspect
from flask_login import UserMixin
from run import app, db, login_manager
# Password hashing.
from passlib.hash import sha256_crypt


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(UserMixin, db.Model):
    """ User Model """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(120), nullable=True)
    jobRole = db.Column(db.String(100), nullable=True)
    currentTeam = db.Column(db.String(100), nullable=True)
    lastUpdatedAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    userRole = db.Column(db.String(8), nullable=False, default="Standard")

    def get_id(self):
        """Return the user id to satisfy Flask-Login's requirements."""
        return self.id


class Skills(db.Model):
    """ Skills Model """
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skillName = db.Column(db.String(120), nullable=False)
    skillRating = db.Column(db.Integer, nullable=False)


class Comments(db.Model):
    """ Comments Model """
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.Column(db.String(120), nullable=True)


def create_database_and_data():
    db.create_all()

    adminUser = db.session.query(Users).filter_by(
        email="mayank.patel@admin.com").first()

    standardUser = db.session.query(Users).filter_by(
        email="mayank.patel@standard.com").first()


    if not standardUser:
        newUser = Users(
            name="Mayank Patel Standard",
            email="mayank.patel@standard.com",
            password=sha256_crypt.encrypt("standard"),
            jobRole="Software Developer - Standard",
            currentTeam="NHS.UK - Service Profiles",
        )
        db.session.add(newUser)
        db.session.commit()

    if not adminUser:
        newUser = Users(
            name="Mayank Patel",
            email="mayank.patel@admin.com",
            password=sha256_crypt.encrypt("admin"),
            jobRole="Software Developer",
            currentTeam="NHS.UK - Service Profiles",
            userRole="Admin",
        )
        db.session.add(newUser)
        db.session.commit()

        registeredUser = db.session.query(Users).filter_by(
            email="mayank.patel@admin.com").first()

        skill_one = Skills(
            userId=registeredUser.id,
            skillName="Kubernetes",
            skillRating=5
        )
        skill_two = Skills(
            userId=registeredUser.id,
            skillName="C# dotnet",
            skillRating=4
        )
        comment = Comments(
            userId=registeredUser.id,
            comments="I also do performance testing for NHS.UK on varies Covid and Non-Covid related services."
        )

        db.session.add(comment)
        db.session.add(skill_one)
        db.session.add(skill_two)
        db.session.commit()
