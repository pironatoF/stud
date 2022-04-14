from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db

from resources.user import(
    UserRegister, User, UserLogin, TokenRefresh, UserLogout)
from resources.item import Item, ItemList
from resources.store import Store, StoreList
import os

from blacklist import BLACKLIST
# import re

# or other relevant config var
uri = os.getenv("DATABASE_URL", "sqlite:///data.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # root folder
# only on flask extension not sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'testest'
app.config['JWT_SECRET_KEY'] = 'test'
api = Api(app)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blocklist_loader
def blocklist_cb(jwt_header, jwt_payload):
    print(jwt_payload)

    identity = jwt_payload.get('sub')
    jti = jwt_payload.get('jti')

    # perform logout
    if jti in BLACKLIST:
        return identity
    # perform blacklist
    if identity and identity in BLACKLIST:
        if jwt_payload.get('type') in ('access', 'refresh'):
            return identity


@jwt.expired_token_loader
def expired_token_cb(jwt_header, jwt_payload):
    return jsonify({
        'message': "The token has expired",
        "error": "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_cb(error):
    return jsonify({
        "message": "Your token is not valid",
        "error": "invalid_token"}), 401


@jwt.unauthorized_loader
def unauthorized_token_cb(error):
    return jsonify({
        "message": "You are not authorized to perform this action",
        "error": "unauthorized_token"}), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_cb(jwt_header, jwt_payload):
    return jsonify({
        "message": f"I'm sorry {jwt_payload['sub']} you have to login in order to perform this action",
        "error": "needs_fresh_token"}), 401


@jwt.revoked_token_loader
def revoked_token_cb(jwt_header, jwt_payload):
    return jsonify({
        "message": f"I'm sorry {jwt_payload['sub']} I can't let you do that",
        "error": "revoked_token"}), 401


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)

"""
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
     'access_token': access_token.decode('utf-8'),
     'user_id': identity.id
     })
"""

"""
@jwt.error_handler
def customized_error_handler(error):
 return jsonify({
     'message': error.description,
     'code': error.status_code
 }), error.status_code
"""
# items: List = []


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

"""
if __name__ == "__main__":
    try:
        app.run(port=5000, debug=True)
    except TimeoutError:
        app.run(port=os.environ['PORT'])
"""
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(port=port)
