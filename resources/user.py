from flask_restful import Resource, reqparse
from models.user import UserModel, Role
import json

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",
                        type =str)
    parser.add_argument("password",
                        type=str)
    def post(self):
        data = User.parser.parse_args(strict=True)

        if UserModel.find_by_name(data["name"]):
            return {"message": "User already exists"}, 400
        else:
            try:
                UserModel(data["name"], data["password"], [Role.find_by_id(1),]).save_to_db()

            except:
                return {"message" : "An error occured"}, 500
            return {"message": "User created"}, 201



    def put(self):
        self.parser.add_argument("roles",
                                 action='append',
                                 )
        data = User.parser.parse_args(strict=True)
        user = UserModel.find_by_name(data["name"])

        if user:

            user.name = data["name"]
            user.password = data["password"]
            user.roles = [Role.find_by_name(x) for x in data["roles"] if Role.find_by_name(x) != None]

            user.save_to_db()

            return {"message": "User updated"}, 200
        else:
            try:
                UserModel(data["name"], data["password"], [Role.find_by_name(x) for x in data["roles"]]).save_to_db()

            except:
                return {"message" : "An error occured"}, 500
            return {"message": "User created"}, 201
