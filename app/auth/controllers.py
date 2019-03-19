from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import get_jwt_identity

from app import app, jwt, db, flask_bcrypt
from app.auth.models import User
from app.auth.schemas import validate_user

auth = Blueprint('auth', __name__)# , url_prefix='/')

@app.route('/', methods=['GET'])
def index():
    return jsonify({'ok': True, 'message': 'pong'}), 401


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({ 'ok': False, 'message': 'Missing authorization header' }), 401


@app.route('/auth', methods=['POST'])
def auth_user():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = User.query.filter_by(name=data['name']).first()
        if user and flask_bcrypt.check_password_hash(user.password, data['password']):
            del user.password
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user.token = access_token
            user.refresh = refresh_token
            return jsonify({'ok': True, 'access_token': access_token, 'refresh_token': refresh_token}), 200
        else:
            return jsonify({'ok': False, 'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/register', methods=['POST'])
def register():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(name=data['name'], email=data['email'], password=data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'ok': True, 'message': 'User created successfully'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = { 'token': create_access_token(identity=current_user) }
    return jsonify({'ok': True, 'data': ret}), 200


@app.route('/user', methods=['GET', 'DELETE', 'PATCH'])
@jwt_required
def user():
    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one(query, {"_id": 0})
        return jsonify({'ok': True, 'data': data}), 200

    data = request.get_json()
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
