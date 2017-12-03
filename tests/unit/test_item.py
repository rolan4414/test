from tests.base_test import BaseTest
from models.item import ItemModel


class TestItemModel(BaseTest):
    def test_init_item(self):
        item = ItemModel("test", 20.0,1)

        self.assertEqual(item.name, "test",
                         "Initializing went wrong!! Item name is diffrent")
        self.assertEqual(item.price, 20.0,
                         "Initializing went wrong!! Item price is diffrent")
