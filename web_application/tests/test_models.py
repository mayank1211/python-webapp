# tests/test_back_end.py
import unittest
from flask import abort, url_for
from flask_testing import TestCase
# Password hashing.
from passlib.hash import sha256_crypt
from run import app, db
from models import Users, Skills, Comments
from create_data import create_database_and_data

class TestBase(TestCase):

    def create_app(self):
        # pass in test configurations
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.app = app.test_client()
        return app

    def setUp(self):
        """
        Create tables and data
        """
        db.session.remove()
        db.drop_all()
        create_database_and_data()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

class TestModels(TestBase):

    def test_admin_user_model(self):
        """
        Test single admin account added to Users table
        """
        adminUser = Users.query.filter_by(userRole="Admin").all()
        
        self.assertEqual(len(adminUser), 1)
        self.assertEqual(adminUser[0].name, "Mayank Patel")
        self.assertEqual(adminUser[0].email, "mayank.patel@admin.com")
        self.assertEqual(adminUser[0].jobRole, "Software Developer")
        self.assertEqual(adminUser[0].userRole, "Admin")
        self.assertEqual(adminUser[0].currentTeam, "NHS.UK - Service Profiles")

    def test_standard_user_model(self):
        """
        Test single standard account added to Users table
        """
        standardUser = Users.query.filter_by(userRole="Standard").all()
        
        self.assertEqual(len(standardUser), 1)
        self.assertEqual(standardUser[0].name, "Mayank Patel Standard")
        self.assertEqual(standardUser[0].email, "mayank.patel@standard.com")
        self.assertEqual(standardUser[0].jobRole, "Software Developer - Standard")
        self.assertEqual(standardUser[0].userRole, "Standard")
        self.assertEqual(standardUser[0].currentTeam, "NHS.UK - Service Profiles")

    def test_skills_model(self):
        """
        Test single skill added to admin account
        """
        userSkill = Skills.query.filter_by(userId=2).all()
        
        self.assertEqual(len(userSkill), 2)
        self.assertEqual(userSkill[0].id, 1)
        self.assertEqual(userSkill[0].userId, 2)
        self.assertEqual(userSkill[0].skillName, "Kubernetes")
        self.assertEqual(userSkill[0].skillRating, 5)

    def test_comments_model(self):
        """
        Test single comment added to admin account
        """
        userComment = Comments.query.filter_by(userId=2).all()
        
        self.assertEqual(len(userComment), 1)
        self.assertEqual(userComment[0].id, 1)
        self.assertEqual(userComment[0].userId, 2)
        self.assertEqual(userComment[0].comments, "I also do performance testing for NHS.UK on varies Covid and Non-Covid related services.")

if __name__ == '__main__':
    unittest.main()
