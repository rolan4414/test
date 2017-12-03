import os

from flask import Flask
from flask_restful import Api



def create_app(Config="DevelopmentConfig"):
    app = Flask(__name__)
    api = Api(app)

    app.config.from_pyfile('settings.py')

    app.config.from_object('settings.'+ Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
    from db import db
    db.init_app(app)

    from resources.item import ItemList, Item

    api.add_resource(ItemList, "/items")
    api.add_resource(Item, "/item/<string:name>")

    from resources.store import Store, StoreList

    api.add_resource(Store, "/store/<string:name>")
    api.add_resource(StoreList, "/store")



    return app




if __name__ == '__main__':
    app = create_app()
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            from db import db
            db.create_all()



    app.run()