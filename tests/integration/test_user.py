from tests.base_test import BaseTest
from models.user import UserModel
from models.user import Role

class TestUserModel(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel("Test","asdf")

            self.assertIsNone(UserModel.find_by_name("Test"))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_name("Test"))

            user.delete_from_db()

            self.assertIsNone(UserModel.find_by_name("Test"))

    def test_relationship_user(self):
        with self.app_context():
            role = Role(name="User")
            role1 = Role(name="Moderator")

            user = UserModel("Test", "asdf", [role, role1])

            self.assertEqual(user.roles[0].name, "User")
            self.assertEqual(user.roles[1].name, "Moderator")

