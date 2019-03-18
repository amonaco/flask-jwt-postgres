from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import datetime

app = Flask(__name__)
# this stuff is actually in config, remove from here
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/auth'
# app.config['JWT_SECRET_KEY'] = 'f9a5112f32a14a39aeef19e8874a9ee7'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=5)

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

@app.errorhandler(405)
def not_found_error(error):
    return jsonify({ 'ok': False, 'message': 'Method not allowed' }), 405


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({ 'ok': False, 'message': 'Not Found' }), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({ 'ok': False, 'message': 'Internal Server Error' }), 500


from app.auth.controllers import auth
app.register_blueprint(auth)

# db.create_all()
