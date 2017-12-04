from flask_restful import Resource, reqparse
from models.user import UserModel

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",
                        type =str)
    parser.add_argument("password",
                        )
    def post(self,):
        data = User.parser.parse_args(strict=True)

        if UserModel.find_by_name(data["name"]):
            return {"message": "User already exists"}, 400
        else:
            try:
                UserModel(data["name"], data["password"]).save_to_db()
            except:
                return {"message" : "An error occured"}, 500
            return {"message": "User created"}, 201

