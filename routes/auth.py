from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User, db
from utils.logger import logger
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 400  # Check for existing user
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    logger.info('New user registered: {}'.format(new_user.username))
    return jsonify({'message': 'User registered'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        logger.info('User logged in: {}'.format(user.username))
        return jsonify(access_token=access_token), 200
    logger.warning('Login failed for user: {}'.format(data['username']))
    return jsonify({'message': 'Invalid username or password'}), 401
