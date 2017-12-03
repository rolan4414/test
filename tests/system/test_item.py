from tests.base_test import BaseTest
from models.item import ItemModel
import json



class ItemTest(BaseTest):

    def test_item_found(self):
        with self.app() as c:
            with self.app_context():
                ItemModel("Test", 20.0, 1).save_to_db()
                r = c.get("/item/Test")

                self.assertEqual(r.status_code, 200)
                expected = {
                    "name" : "Test",
                    "price": 20.0,
                }
                self.assertDictEqual(json.loads(r.data), expected)
    def test_item_no_found(self):
        with self.app() as c:
            with self.app_context():
                r = c.get("/item/Test")

                self.assertEqual(r.status_code, 404)
    def test_create_item(self):
        with self.app() as c:
            with self.app_context():
                r = c.post("/item/Test", headers = {"Content-Type": "application/json"}, data =json.dumps({"price": 20.0, "store_id": 1}))

                self.assertEqual(r.status_code, 201)

                self.assertIsNotNone(ItemModel.find_by_name("Test"))

    def test_create_duplicate(self):
        with self.app() as c:
            with self.app_context():
                ItemModel("Test", 20.0, 1).save_to_db()

                r = c.post("/item/Test", headers={"Content-Type": "application/json"}, data=json.dumps({"price": 20.0}))

                self.assertEqual(r.status_code, 400)

                self.assertIsNotNone(ItemModel.find_by_name("Test"))
                self.assertEqual(json.loads(r.data), {"message":"Item already exists!!"})


    def test_delete(self):
        with self.app() as c:
            with self.app_context():
                ItemModel("Test", 20.0, 1).save_to_db()

                r = c.delete("/item/Test")

                self.assertEqual(r.status_code, 200)

                self.assertIsNone(ItemModel.find_by_name("Test"))


    def test_put_update_item(self):
        with self.app() as c:
            with self.app_context():
                ItemModel("Test", 20.0, 1).save_to_db()

                r = c.put("/item/Test", headers={"Content-Type": "application/json"}, data=json.dumps({"price": 21.0}))

                self.assertEqual(r.status_code, 200)

                self.assertIsNotNone(ItemModel.find_by_name("Test"))
                self.assertEqual(ItemModel.find_by_name("Test").price, 21.0)


    def test_put_item(self):
        with self.app() as c:
            with self.app_context():

                r = c.put("/item/Test", headers={"Content-Type": "application/json"}, data=json.dumps({"price": 21.0, "store_id" : 1}))

                self.assertEqual(r.status_code, 200)

                self.assertIsNotNone(ItemModel.find_by_name("Test"))
                self.assertEqual(ItemModel.find_by_name("Test").price, 21.0)
