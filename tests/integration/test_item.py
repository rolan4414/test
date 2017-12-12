from tests.base_test import BaseTest
from models.item import ItemModel
from models.store import StoreModel

class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel("Test1").save_to_db()

            item = ItemModel("test", 20.0, 1)

            self.assertIsNone(ItemModel.find_by_name("test"))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name("test"))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name("test"))

    def test_relation_backref(self):
        with self.app_context():
            StoreModel("test").save_to_db()

            ItemModel("test", 20, 1).save_to_db()

            self.assertEqual(ItemModel.find_by_name("test").shop.name, "test")
