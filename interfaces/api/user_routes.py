from flask import Blueprint, request, jsonify
from application.services.user_service import UserService
from infra.repositories.users_database import UserDB

user_service = UserService(UserDB())
user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        user = user_service.create_user_with_password(data['username'], data['email'], data['password'])
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_service.login_user(data['email'], data['password'])
    if user:
        return jsonify({'message': 'Login successful', 'user': {'id': user.id, 'username': user.username, 'email': user.email}})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401