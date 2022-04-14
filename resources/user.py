from flask_restful import Resource, reqparse
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import(
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required, get_jwt)
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help="This field cannot be left blank!"
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help="This field cannot be left blank!"
)


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data.get('username')):
            return {'message': 'User already exist'}, 400
        user = UserModel(**data)
        user.save()
        return {"message": "User created"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete()
        return {"message": "User deleted"}, 200


class UserLogin(Resource):
    def post(self):
        """ create access_token/refresh_token """
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data.get('username'))
        if not user:
            return {'message': 'User not exist'}, 401
        if not compare_digest(user.password, data.get('password')):
            return {'message': "Password mismatch"}, 401
        if user.username in BLACKLIST:
            return {'message': "Your account has been banned"}, 401
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        """ nota il set si puo trasformare in un redis """
        print(BLACKLIST)
        BLACKLIST.add(get_jwt().get('jti'))
        return {'message': "Logged out"}, 200


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)
        return {'access_token': new_token}, 200
