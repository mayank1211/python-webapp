import datetime
import sqlalchemy
from flask import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db = sqlalchemy(app)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

class User(db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    currentTeam = db.Column(db.String(50), nullable=True)
    lastUpdatedAt = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=True)


class Skills(db.Model):
    """Skills model"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    authorId = db.Column(db.Integer, foreign_key=True)
    skillName = db.Column(db.String(50), nullable=True)
    skillRating = db.Column(db.Integer(5), nullable=True)


class Comments(db.Model):
    """Comments model"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    authorId = db.Column(db.Integer, foreign_key=True)
    comments = db.Column(db.String(500), nullable=False)
