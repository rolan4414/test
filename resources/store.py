from flask_restful import Resource

from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        else:
            return {"message": "Item not found"}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "Item already exist"}, 400
        else:
            try:
                StoreModel(name).save_to_db()
            except:
                return {"message": "An error occured"}, 500
            return {"message": "Item created!"}, 201

    def delete(self, name):
        if item:
                StoreModel.find_by_name(name).delete_from_db()
        return {"message": "Item deleted!"}, 200

class StoreList(Resource):
    def get(self):
        stores = [x.name for x in StoreModel.query.all()]
        return {"stores": stores}