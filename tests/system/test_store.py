import json

from tests.base_test import BaseTest

from models.store import StoreModel
from models.item import ItemModel

class StoreTest(BaseTest):
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