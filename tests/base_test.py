from unittest import TestCase
from app import create_app
from db import db


app = create_app()
class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.from_object('settings.TestingConfig')

    def setUp(self):
        with app.app_context():
            db.create_all()

        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
