from tests.base_test import BaseTest
from models.user import UserModel


class TestUserModel(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel("Test","asdf")

            self.assertIsNone(UserModel.find_by_name("Test"))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_name("Test"))

            user.delete_from_db()

            self.assertIsNone(UserModel.find_by_name("Test"))