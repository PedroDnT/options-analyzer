"""
User management routes
"""

from flask import Blueprint, request, jsonify
from src.models.user import User, db
import logging

logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch users'
        }), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Input validation
        if not data or not data.get('username') or not data.get('email'):
            return jsonify({
                'success': False,
                'error': 'Username and email are required'
            }), 400
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == data['username']) | 
            (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'User with this username or email already exists'
            }), 409
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to create user'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        # Input validation
        if not isinstance(user_id, int) or user_id <= 0:
            return jsonify({
                'success': False,
                'error': 'Invalid user ID'
            }), 400
        
        user = User.query.get_or_404(user_id)
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404