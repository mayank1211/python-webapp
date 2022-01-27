import datetime
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy import inspect

metadata = MetaData()

users = Table('users', metadata,
  Column('Id', Integer, primary_key=True, autoincrement=True),
  Column('Name', String(50)),
  Column('Email', String(100)),
  Column('Password', String),
  Column('Role', String(50)),
  Column('CurrentTeam', String(50)),
  Column('LastUpdatedAt', DateTime, default=datetime.datetime.utcnow),
)

skills = Table('skills', metadata,
  Column('Id', Integer, primary_key=True, autoincrement=True),
  Column('UserId', String, ForeignKey("users.Id")),
  Column('SkillName', String(30), nullable=False),
  Column('SkillRating', Integer, nullable=False)
)

comments = Table('comments', metadata,
  Column('Id', Integer, primary_key=True, autoincrement=True),
  Column('UserId', Integer, ForeignKey("users.Id")),
  Column('Comments', String(500), nullable=False)
)