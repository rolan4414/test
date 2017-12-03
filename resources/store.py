from flask_restful import Resource

from models.store import StoreModel

class Store(Resource):
    store = StoreModel.find_by_name(name)

    def get(self, name):

        if self.store:
            return store.json()
        else:
            return {"message": "Item not found"}

    def post(self, name):
        store
