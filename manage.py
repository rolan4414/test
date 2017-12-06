# manage.py


import unittest

from flask_script import Manager

from app import create_app
from db import db
from models.user import Role, UserModel


app = create_app()
manager = Manager(app)



@manager.command
def test():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """Seeds the database."""
    Role(name="User").save_to_db()
    Role(name="Moderator").save_to_db()
    Role(name="Administrator").save_to_db()
    UserModel("Admin","admin",[Role.find_by_id(3),Role.find_by_id(2), Role.find_by_id(1)])






if __name__ == '__main__':
    manager.run()
