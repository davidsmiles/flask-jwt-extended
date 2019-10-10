from flask import jsonify
from flask_restful import Resource, reqparse


class Index(Resource):

    def get(self):
        return jsonify(message='Welcome to Stores-REST API')