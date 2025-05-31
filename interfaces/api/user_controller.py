
from flask import Blueprint, jsonify
from application.services.user_service import UserService
from infra.repositories.user_repository import InMemoryUserRepository

user_bp = Blueprint('user', __name__)
user_service = UserService(InMemoryUserRepository())

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404