from models.base_model import BaseModel
from db import db



class StoreModel(db.Model, BaseModel):

    __tablename__ = "stores"

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
