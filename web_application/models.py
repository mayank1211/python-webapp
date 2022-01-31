import datetime
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy import inspect
from flask_login import UserMixin
from web_application import app, db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

class Users(UserMixin, db.Model):
    """ User Model """
    __tablename__ = "users"
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(80), nullable=True)
    Email = db.Column(db.String(120), nullable=True)
    Password = db.Column(db.String(120), nullable=True)
    Role = db.Column(db.String(100), nullable=True)
    CurrentTeam = db.Column(db.String(100), nullable=True)
    LastUpdatedAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def get_id(self):
        """Return the user id to satisfy Flask-Login's requirements."""
        return self.Id



class Skills(db.Model):
    """ Skills Model """
    __tablename__ = "skills"
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('users.Id'), nullable=False)
    SkillName = db.Column(db.String(120), nullable=False)
    SkillRating = db.Column(db.Integer, nullable=False)

class Comments(db.Model):
    """ Comments Model """
    __tablename__ = "comments"
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('users.Id'), nullable=False)
    Comments = db.Column(db.String(120), nullable=True)


db.create_all()