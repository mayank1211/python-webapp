import datetime
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy import inspect

from web_application import app, db

class Users(db.Model):
    """ User Model """
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(80), nullable=True)
    Email = db.Column(db.String(120), nullable=True)
    Password = db.Column(db.String(120), nullable=True)
    Role = db.Column(db.String(100), nullable=True)
    CurrentTeam = db.Column(db.String(100), nullable=True)
    LastUpdatedAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
      return self._repr(
        Id=self.Id,
        Name=self.Name,
        Email=self.Email,
        Password=self.Password,
        Role=self.Role,
        CurrentTeam=self.CurrentTeam,
        LastUpdatedAt=self.LastUpdatedAt
      )

class Skills(db.Model):
    """ Skills Model """
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('users.Id'), nullable=False)
    SkillName = db.Column(db.String(120), nullable=False)
    SkillRating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
      return self._repr(
        Id=self.Id,
        UserId=self.Name,
        SkillName=self.Email,
        SkillRating=self.Password
      )

class Comments(db.Model):
    """ Comments Model """
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('users.Id'), nullable=False)
    Comments = db.Column(db.String(120), nullable=True)

    def __repr__(self):
      return self._repr(
        Id=self.Id,
        UserId=self.Name,
        Comments=self.Email
      )

