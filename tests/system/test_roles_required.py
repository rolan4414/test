import json

from tests.base_test import BaseTest

from models.store import StoreModel
from models.user import UserModel, Role


class RoleRequired(BaseTest):
    def test_correct_role_create(self):

        with self.app() as c:
            with self.app_context():
                role = Role(name="Moderator")
                role.save_to_db()
                UserModel("Test", "asdf", [role,]).save_to_db()

                r = c.post("/auth", headers = {"Content-Type": "application/json"} , data =json.dumps({"username":"Test",
                                                                                                    "password": "asdf"}))
                auth_key = "JWT {}".format(json.loads(r.data)["access_token"])

                r = c.post("/store/Test", headers={"Authorization" : auth_key})

                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("Test"))

    def test_incorrect_role_create(self):
        with self.app() as c:
            with self.app_context():
                role = Role(name="User")
                role.save_to_db()
                UserModel("Test", "asdf", [role,]).save_to_db()

                r = c.post("/auth", headers = {"Content-Type": "application/json"} , data =json.dumps({"username":"Test",
                                                                                                    "password": "asdf"}))
                auth_key = "JWT {}".format(json.loads(r.data)["access_token"])

                r = c.post("/store/Test", headers={"Authorization" : auth_key})

                self.assertEqual(r.status_code, 404)
                self.assertIsNone(StoreModel.find_by_name("Test"))
                self.assertDictEqual(json.loads(r.data), {"message": "You're not allowed to enter"}
)