import json

from tests.base_test import BaseTest

from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel, Role


class StoreTest(BaseTest):
    def setUp(self):
        super(StoreTest,self).setUp()
        with self.app() as c:
            with self.app_context():
                role = Role(name="Moderator")
                role.save_to_db()
                UserModel("Test", "asdf", [role,]).save_to_db()

                r = c.post("/auth", headers = {"Content-Type": "application/json"} , data =json.dumps({"username":"Test",
                                                                                                    "password": "asdf"}))
                self.auth_key = "JWT {}".format(json.loads(r.data)["access_token"])



    def test_get_store_found(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test").save_to_db()

                r = c.get("/store/Test")

                expected = {
                    "items": [],
                    "name": "Test"
                }
                self.assertDictEqual(expected, json.loads(r.data))
    def test_get_store_not_found(self):
        with self.app() as c:
            with self.app_context():

                r = c.get("/store/Test")

                expected = {
                    "message": "Item not found"
                }
                self.assertDictEqual(expected, json.loads(r.data))

    def test_get_store_with_items(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test").save_to_db()

                ItemModel("Test1", 21, 1).save_to_db()
                ItemModel("Test2", 22, 1).save_to_db()


                r = c.get("/store/Test")

                expected = {
                    "items": ["Test1", "Test2"],
                    "name": "Test"
                }


                self.assertDictEqual(expected, json.loads(r.data))
    def test_get_all_items(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test1").save_to_db()
                StoreModel("Test2").save_to_db()
                StoreModel("Test3").save_to_db()
                StoreModel("Test4").save_to_db()
                StoreModel("Test5").save_to_db()

                r = c.get("/store")


                expected = {
                    "stores":
                        ["Test1",
                         "Test2",
                         "Test3",
                         "Test4",
                         "Test5"]
                }
                self.assertDictEqual(expected, json.loads(r.data))

    def test_create_item(self):
        with self.app() as c:
            with self.app_context():

                r = c.post("/store/Test", headers={"Authorization" : self.auth_key})

                self.assertIsNotNone(StoreModel.find_by_name("Test"))
                self.assertEqual(r.status_code, 201)

    def test_create_duplicate_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test").save_to_db()
                r = c.post("/store/Test", headers={"Authorization" : self.auth_key})


                self.assertIsNotNone(StoreModel.find_by_name("Test"))
                self.assertEqual(r.status_code, 400)


    def test_delete_item(self):
        with self.app() as c:
            with self.app_context():

                StoreModel("Test").save_to_db()

                r = c.delete("/store/Test")
                self.assertIsNone(StoreModel.find_by_name("Test"))

