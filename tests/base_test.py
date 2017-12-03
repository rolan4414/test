from unittest import TestCase
from app import create_app
from db import db

app = create_app()
class BaseTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"


    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = BaseTest.SQLALCHEMY_DATABASE_URI
        app.config['DEBUG'] = False



    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
