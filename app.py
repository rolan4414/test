from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, JWTError, jsonify


def create_app(Config="DevelopmentConfig"):
    app = Flask(__name__)
    api = Api(app)


    app.config.from_object('settings.'+ Config)
    from db import db
    db.init_app(app)

    from resources.item import ItemList, Item
    from resources.store import Store, StoreList
    from resources.user import User

    api.add_resource(ItemList, "/items/<int:page>",
                     "/items")
    api.add_resource(Item, "/item/<string:name>")

    api.add_resource(Store, "/store/<string:name>")
    api.add_resource(StoreList, "/store")

    api.add_resource(User, "/user")



    from security import authenticate, identity
    jwt = JWT(app, authenticate, identity)

    @app.errorhandler(JWTError)
    def auth_error_handler(err):
        return jsonify({"message": "Couldnt not authorize"}), 401

    return app


if __name__ == '__main__':
    app = create_app()

    app.run()