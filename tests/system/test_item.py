from tests.base_test import BaseTest
from models.item import ItemModel
from models.store import StoreModel
import json



class ItemTest(BaseTest):
    def test_item_found(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test1").save_to_db()

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
                StoreModel("Test").save_to_db()

                r = c.post("/item/Test", headers = {"Content-Type": "application/json"}, data =json.dumps({"price": 20.0, "store_id": 1}))

                self.assertEqual(r.status_code, 201)

                self.assertIsNotNone(ItemModel.find_by_name("Test"))

    def test_create_duplicate(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test1").save_to_db()
                ItemModel("Test", 20.0, 1).save_to_db()

                r = c.post("/item/Test", headers={"Content-Type": "application/json"}, data=json.dumps({"price": 20.0}))

                self.assertEqual(r.status_code, 400)

                self.assertIsNotNone(ItemModel.find_by_name("Test"))
                self.assertEqual(json.loads(r.data), {"message":"Item already exists!!"})


    def test_delete(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test1").save_to_db()
                ItemModel("Test", 20.0, 1).save_to_db()

                r = c.delete("/item/Test")

                self.assertEqual(r.status_code, 200)

                self.assertIsNone(ItemModel.find_by_name("Test"))


    def test_put_update_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test1").save_to_db()

                ItemModel("Test", 20.0, 1).save_to_db()

                r = c.put("/item/Test", headers={"Content-Type": "application/json"}, data=json.dumps({"price": 21.0}))

                self.assertEqual(r.status_code, 200)

                self.assertIsNotNone(ItemModel.find_by_name("Test"))
                self.assertEqual(ItemModel.find_by_name("Test").price, 21.0)


    def test_put_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test1").save_to_db()

                r = c.put("/item/Test", headers={"Content-Type": "application/json"}, data=json.dumps({"price": 21.0, "store_id" : 1}))

                self.assertEqual(r.status_code, 200)

                self.assertIsNotNone(ItemModel.find_by_name("Test"))
                self.assertEqual(ItemModel.find_by_name("Test").price, 21.0)



    def test_get_all_items(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test1").save_to_db()

                ItemModel("Test1", 21.0, 1).save_to_db()
                ItemModel("Test2", 22.0, 1).save_to_db()
                ItemModel("Test3", 23.0, 1).save_to_db()

                r = c.get("/items")


                self.assertEqual(json.loads(r.data)["page info"]["total items"], 3)

                self.assertDictEqual(json.loads(r.data)["items"][0], {"price" : 21.0,
                                                                      "name" : "Test1"})
                self.assertDictEqual(json.loads(r.data)["items"][1], {"price" : 22.0,
                                                                      "name" : "Test2"})
                self.assertDictEqual(json.loads(r.data)["items"][2], {"price" : 23.0,
                                                                      "name" : "Test3"})
    def test_pagination_first_page(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test1").save_to_db()

                [ItemModel("Test"+str(x), 20+x, 1).save_to_db() for x in range(21)]

                r = c.get("/items/1")

                self.assertEqual(json.loads(r.data)["items"][-1]["name"],"Test19")
                self.assertEqual(len(json.loads(r.data)["items"]), 20)
                self.assertEqual(json.loads(r.data)["page info"]["next page"],2)
                self.assertEqual(json.loads(r.data)["page info"]["total items"],21)
                self.assertEqual(json.loads(r.data)["page info"]["pages"],2)

    def test_pagination_second_page(self):
        with self.app() as c:
            with self.app_context():
                StoreModel("Test1").save_to_db()

                [ItemModel("Test"+str(x), 20+x, 1).save_to_db() for x in range(21)]

                r = c.get("/items/2")

                self.assertEqual(json.loads(r.data)["items"][0]["name"],"Test20")
                self.assertEqual(len(json.loads(r.data)["items"]),1)
                self.assertIsNone(json.loads(r.data)["page info"]["next page"])
                self.assertEqual(json.loads(r.data)["page info"]["previous page"],1)
                self.assertEqual(json.loads(r.data)["page info"]["total items"],21)
                self.assertEqual(json.loads(r.data)["page info"]["pages"],2)
