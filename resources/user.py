from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)

from blacklist import BLACKLIST
from models.user import UserModel
from werkzeug.security import safe_str_cmp

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    def get(self, username):
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': 'user not found'}, 404

        return user.json()

    def delete(self, username):
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': 'user not found'}, 404

        return user.delete()


class UsersList(Resource):
    def get(self):
        users = UserModel.find_all()
        return {'users': [user.json() for user in users]}


class UserLogin(Resource):

    def post(self):
        data = _user_parser.parse_args()
        username = data['username']
        password = data['password']

        user = UserModel.find_by_username(username)
        if user and safe_str_cmp(password, user.password):
            access_token = create_access_token(identity=username, fresh=True)
            refresh_token = create_refresh_token(identity=username)
            return jsonify(
                access_token=access_token,
                refresh_token=refresh_token,
                logged_in_as=username
            )
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'successfully logged out'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        if user_id:
            new_token = create_access_token(identity=user_id, fresh=False)
            return {
                'access_token': new_token
            }