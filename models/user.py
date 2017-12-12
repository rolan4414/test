from models.base_model import BaseModel
from db import db

class UserModel(db.Model, BaseModel):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20) )
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, name, password, roles=[]):
        self.name = name
        self.password = password
        self.roles = roles


class Role(db.Model, BaseModel):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)



class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
