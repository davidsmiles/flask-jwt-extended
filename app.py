import os

from flask import Flask
from flask_jwt_extended import *
from flask_restful import Api

from resources.index import Index
from resources.item import *
from resources.store import *
from resources.user import *

app = Flask(__name__)
db_uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = 'secret-key'     # change this in production
api = Api(app)


jwt = JWTManager(app)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    user = UserModel.find_by_username(identity)
    return user if user else None


@jwt.user_loader_error_loader
def user_error_callback(identity):
    return {'message': "user with {} not found..".format(identity)}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted):
    return decrypted['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return {
        'description': 'the token has expired',
        'error': 'token_expired'
    }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }, 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return {
        'description': 'You are not authorized',
        'error': 'unauthorized'
    }, 401


@jwt.needs_fresh_token_loader
def needs_fresh_token():
    return {
        'description': 'Fresh token required',
        'error': 'needs_fresh_token'
    }, 401


@jwt.revoked_token_loader
def revoked_token():
    return {
       'description': 'Token revoked',
       'error': 'revoked_token'
   }, 401


api.add_resource(Index, '/')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:name>')
api.add_resource(UsersList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
