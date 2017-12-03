from db import db



class StoreModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    items = db.relationship('ItemModel', backref = "shop",
                            lazy = True)
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def json(self):
        return {"name": self.name, "items" : [str(x) for x in StoreModel.find_by_name(self.name).items]}


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

