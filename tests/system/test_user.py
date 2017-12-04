import json

from tests.base_test import BaseTest
from models.user import UserModel



class TestUser(BaseTest):
    def test_create_item(self):
        with self.app() as c:
            with self.app_context():

                r = c.post("/user", headers={"Content-Type":"application/json"}, data = json.dumps({"name" : "Test",
                                                                                                "password" : "asdf"}))
                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_name("Test"))

    def test_create_duplicate_item(self):
        with self.app() as c:
            with self.app_context():
                UserModel("Test", "asdf").save_to_db()

                r = c.post("/user", headers={"Content-Type":"application/json"}, data = json.dumps({"name" : "Test",
                                                                                                "password" : "asdf"}))
                self.assertEqual(r.status_code, 400)
                self.assertIsNotNone(UserModel.find_by_name("Test"))
                self.assertEqual(json.loads(r.data), {"message" : "User already exists"})