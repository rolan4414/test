import json

from tests.base_test import BaseTest
from models.user import UserModel, Role



class TestUser(BaseTest):
    def test_create_item(self):
        with self.app() as c:
            with self.app_context():
                Role(name = "User").save_to_db()

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

    def test_update_user(self):
        with self.app() as c:
            with self.app_context():
                UserModel("Test", "asdf").save_to_db()

                Role(name = "User").save_to_db()
                Role(name = "Moderator").save_to_db()

                r = c.put("/user", headers={"Content-Type":"application/json"}, data = json.dumps({"name" : "Test",
                                                                                                "password" : "asdf",
                                                                                                   "roles": ["User","Moderator"] }))
                self.assertEqual(r.status_code, 200)
                self.assertIsNotNone(UserModel.find_by_name("Test"))
                self.assertEqual(json.loads(r.data), {"message" : "User updated"})
                self.assertEqual(UserModel.find_by_name("Test").roles, [Role.find_by_name("User"), Role.find_by_name("Moderator")] )

    def test_put_create_user(self):
        with self.app() as c:
            with self.app_context():

                Role(name = "User").save_to_db()
                Role(name = "Moderator").save_to_db()


                r = c.put("/user", headers={"Content-Type":"application/json"}, data = json.dumps({"name" : "Test",
                                                                                                "password" : "asdf",
                                                                                                   "roles": ["User","Moderator"] }))
                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_name("Test"))
                self.assertEqual(json.loads(r.data), {"message" : "User created"})
                self.assertEqual(UserModel.find_by_name("Test").roles, [Role.find_by_name("User"), Role.find_by_name("Moderator")] )
