from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, User
from app.auth import require_auth, require_role, require_ownership_or_role

user_bp = Blueprint('user_bp', __name__)
user_api = Api(user_bp)

class UserListResource(Resource):
    @require_role('admin')
    def get(self):
        """Get all users - Admin only"""
        users = User.query.filter_by(deleted_at=None).all()
        return [{
            'id': u.id,
            'role': u.role.value,
            'email': u.email,
            'full_name': u.full_name,
            'phone': u.phone,
            'location': u.location,
            'is_verified': u.is_verified,
            'created_at': u.created_at.isoformat() if u.created_at else None
        } for u in users]
    
    @require_role('admin')
    def post(self):
        """Create new user - Admin only (for admin user creation)"""
        data = request.json
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return {'id': user.id}, 201

class UserResource(Resource):
    @require_ownership_or_role('user_id', 'admin')
    def get(self, user_id):
        """Get user profile - Owner or Admin only"""
        user = User.query.get_or_404(user_id)
        return {
            'id': user.id,
            'role': user.role.value,
            'email': user.email,
            'full_name': user.full_name,
            'phone': user.phone,
            'location': user.location,
            'description': user.description,
            'is_verified': user.is_verified,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
    
    @require_ownership_or_role('user_id', 'admin')
    def put(self, user_id):
        """Update user profile - Owner or Admin only"""
        user = User.query.get_or_404(user_id)
        data = request.json
        
        # Update allowed fields
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'location' in data:
            user.location = data['location']
        if 'description' in data:
            user.description = data['description']
        if 'is_verified' in data and session.get('user_role') == 'admin':
            user.is_verified = data['is_verified']
        
        db.session.commit()
        return {
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'role': user.role.value,
                'email': user.email,
                'full_name': user.full_name,
                'phone': user.phone,
                'location': user.location,
                'description': user.description,
                'is_verified': user.is_verified
            }
        }, 200
    
    @require_ownership_or_role('user_id', 'admin')
    def delete(self, user_id):
        """Soft delete user - Owner or Admin only"""
        user = User.query.get_or_404(user_id)
        from datetime import datetime
        user.deleted_at = datetime.utcnow()
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200

user_api.add_resource(UserListResource, '/')
user_api.add_resource(UserResource, '/<user_id>')