from flask_restful import Resource, reqparse
from models.item import ItemModel
from models.store import StoreModel



class ItemList(Resource):
    def get(self):
        Item_list = [x.json() for x in ItemModel.query.all()]
        return {"items": Item_list,}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        )
    parser.add_argument('store_id',
                        type=int,
                        )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message" : "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):

            return {"message" : "Item already exists!!"}, 400
        else:

            data = Item.parser.parse_args()

            try:
                StoreModel("test").save_to_db()
                ItemModel(name, data['price'], data['store_id'] ).save_to_db()
            except:
                return {"message" : "An error occured"}, 500

            return {"message" : "Item has been created"}, 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message" : "Item has been Deleted"}, 200



    def put(self, name):
        item = ItemModel.find_by_name(name)

        data = Item.parser.parse_args()

        if item is None:
            item = ItemModel(name, data['price'], data["store_id"])
        else:
            item.price = data["price"]
            item.store = data["store_id"]

        item.save_to_db()

        return item.json()