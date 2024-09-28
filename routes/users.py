from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.user import User, db
from utils.logger import logger
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()  # Initialize Bcrypt

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.active = not user.active  # Toggle active status
        db.session.commit()
        logger.info('User {} active status toggled to {}'.format(user.username, user.active))
        return jsonify({'message': 'User active status toggled'}), 200
    return jsonify({'message': 'User not found'}), 404

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.username = data.get('username', user.username)
        if 'password' in data:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')  # Hashing the new password
        user.role = data.get('role', user.role)
        db.session.commit()
        logger.info('User {} updated'.format(user.username))
        return jsonify({'message': 'User updated'}), 200
    return jsonify({'message': 'User not found'}), 404
