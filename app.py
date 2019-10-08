from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import *
from resources.item import *
from resources.store import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    """
    Claims are just piecies of data that we can choose to attach to the JWT poayload
    Used to add some extra data
    :param identity:
    :return json message telling us whether the current logged in user is the Admin:
    """
    if identity == 1:   # instead of hard coding, you should get the data from a config file or database
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:name>')
api.add_resource(UsersList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
