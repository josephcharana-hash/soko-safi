"""
User routes for Soko Safi
Handles user CRUD operations and artisan payment methods
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, User, UserRole, PaymentMethod
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
            'email': u.email,
            'full_name': u.full_name,
            'role': u.role.value if u.role else None,
            'phone': u.phone,
            'is_verified': u.is_verified,
            'created_at': u.created_at.isoformat() if u.created_at else None
        } for u in users]

    @require_role('admin')
    def post(self):
        """Create new user - Admin only"""
        data = request.json

        user = User(**data)
        db.session.add(user)
        db.session.commit()

        return {
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role.value if user.role else None
            }
        }, 201

class UserResource(Resource):
    @require_ownership_or_role('user_id', 'admin')
    def get(self, user_id):
        """Get user details - Owner or Admin only"""
        user = User.query.get_or_404(user_id)

        return {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role.value if user.role else None,
            'phone': user.phone,
            'description': user.description,
            'profile_picture_url': user.profile_picture_url,
            'banner_image_url': user.banner_image_url,
            'location': user.location,
            'is_verified': user.is_verified,
            'payment_method': user.payment_method.value if user.payment_method else None,
            'mpesa_phone': user.mpesa_phone,
            'paybill_number': user.paybill_number,
            'paybill_account': user.paybill_account,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }

    @require_ownership_or_role('user_id', 'admin')
    def put(self, user_id):
        """Update user - Owner or Admin only"""
        user = User.query.get_or_404(user_id)
        data = request.json

        # Update basic fields
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'description' in data:
            user.description = data['description']
        if 'location' in data:
            user.location = data['location']

        # Update artisan payment method fields (only for artisans)
        if user.role == UserRole.artisan:
            if 'payment_method' in data:
                user.payment_method = PaymentMethod(data['payment_method'])
            if 'mpesa_phone' in data:
                user.mpesa_phone = data['mpesa_phone']
            if 'paybill_number' in data:
                user.paybill_number = data['paybill_number']
            if 'paybill_account' in data:
                user.paybill_account = data['paybill_account']

        db.session.commit()

        return {
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'payment_method': user.payment_method.value if user.payment_method else None,
                'mpesa_phone': user.mpesa_phone,
                'paybill_number': user.paybill_number,
                'paybill_account': user.paybill_account
            }
        }, 200

    @require_role('admin')
    def delete(self, user_id):
        """Delete user - Admin only"""
        user = User.query.get_or_404(user_id)

        from datetime import datetime
        user.deleted_at = datetime.utcnow()
        db.session.commit()

        return {'message': 'User deleted successfully'}, 200

class UserPaymentMethodResource(Resource):
    @require_ownership_or_role('user_id', 'admin')
    def put(self, user_id):
        """Update artisan payment method - Owner or Admin only"""
        user = User.query.get_or_404(user_id)

        if user.role != UserRole.artisan:
            return {'error': 'Only artisans can set payment methods'}, 400

        data = request.json

        if 'payment_method' not in data:
            return {'error': 'Payment method is required'}, 400

        try:
            user.payment_method = PaymentMethod(data['payment_method'])

            if data['payment_method'] == 'phone':
                if 'mpesa_phone' not in data:
                    return {'error': 'M-Pesa phone number is required for phone payments'}, 400
                user.mpesa_phone = data['mpesa_phone']
                user.paybill_number = None
                user.paybill_account = None

            elif data['payment_method'] == 'paybill':
                if 'paybill_number' not in data or 'paybill_account' not in data:
                    return {'error': 'Paybill number and account are required for paybill payments'}, 400
                user.paybill_number = data['paybill_number']
                user.paybill_account = data['paybill_account']
                user.mpesa_phone = None

            db.session.commit()

            return {
                'message': 'Payment method updated successfully',
                'payment_method': user.payment_method.value,
                'mpesa_phone': user.mpesa_phone,
                'paybill_number': user.paybill_number,
                'paybill_account': user.paybill_account
            }, 200

        except ValueError as e:
            return {'error': f'Invalid payment method: {str(e)}'}, 400

# Register routes
user_api.add_resource(UserListResource, '/')
user_api.add_resource(UserResource, '/<user_id>')
user_api.add_resource(UserPaymentMethodResource, '/<user_id>/payment-method')