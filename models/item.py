from models.base_model import BaseModel
from db import db



class ItemModel(db.Model, BaseModel):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    price = db.Column(db.Float(precision = 2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'),
                         nullable=False)

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def __repr__(self):
        return self.name


    def json(self):
        return {"name": self.name, "price" : self.price}
