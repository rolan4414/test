from db import db


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20) )
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, name, password, roles=[]):
        self.name = name
        self.password = password
        self.roles = roles

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

        def save_to_db(self):
            db.session.add(self)
            db.session.commit()

        def delete_from_db(self):
            db.session.delete(self)
            db.session.commit()

        @classmethod
        def find_by_name(cls, name):
            return cls.query.filter_by(name=name).first()

        @classmethod
        def find_by_id(cls, _id):
            return cls.query.filter_by(id=_id).first()


class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))