from tests.base_test import BaseTest
from models.user import UserModel

class TestUserModel(BaseTest):
    def test_init_method(self):
        user = UserModel("Test", "asdf")

        self.assertEqual(user.name, "Test")
        self.assertEqual(user.password, "asdf")