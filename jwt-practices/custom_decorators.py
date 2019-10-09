from flask import *
from flask_jwt_extended import *

from functools import wraps


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret-key'
jwt = JWTManager(app)


def admin_required(fn):
    @wraps(fn)
    def secure_func(*args, **kwargs):
        verify_jwt_in_request()
        user = get_jwt_claims()
        if 'admin' in user['roles']:
            return fn(*args, **kwargs)
        else:
            return {'message': 'for admin only, forbidden'}, 403
    return secure_func


@jwt.unauthorized_loader
def unauthorized(error):
    return jsonify(message='you are not authorized bro')


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    if identity == 'admin':
        return {'roles': 'admin'}
    else:
        return {'roles': 'peasant'}


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    access_token = create_access_token(username)
    return jsonify(access_token=access_token)


@app.route('/protected', methods=['GET'])
@admin_required
def protected():
    return jsonify(secret_message="go banana!")


if __name__ == '__main__':
    app.run()