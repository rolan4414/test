from tests.base_test import BaseTest
from models.item import ItemModel
from models.store import StoreModel

class TestStoreModel(BaseTest):
    def test_init_object(self):
        store = StoreModel("Test")

        self.assertEqual(store.name, "Test")
