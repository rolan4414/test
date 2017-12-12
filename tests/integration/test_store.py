from tests.base_test import BaseTest
from models.item import ItemModel
from models.store import StoreModel

class TestModelStore(BaseTest):
    def test_crud(self):
        with self.app_context():
            store = StoreModel("test")

            self.assertIsNone(StoreModel.find_by_name("test"))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name("test"))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name("test"))

    def test_relationship(self):
        with self.app_context():
            StoreModel("test").save_to_db()

            ItemModel("Test1",21,1).save_to_db()
            ItemModel("Test2",23,1).save_to_db()

            self.assertEqual(StoreModel.find_by_name("test").items,
                             [ItemModel.find_by_name("Test1"),
                              ItemModel.find_by_name("Test2")])

    def test_json(self):
        with self.app_context():

            store = StoreModel("test")
            store.save_to_db()

            ItemModel("Test1", 21, 1).save_to_db()
            ItemModel("Test2", 21, 1).save_to_db()


            expected = {"name": "test", "items" : ["Test1",
                                                   "Test2"]}

            self.assertDictEqual(expected, store.json())
