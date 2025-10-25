"""
Payment routes for Soko Safi
Handles CRUD operations for payments
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Payment, PaymentMethod, PaymentStatus
from app.auth import require_auth, require_role, require_ownership_or_role

payment_bp = Blueprint('payment_bp', __name__)
payment_api = Api(payment_bp)

class PaymentListResource(Resource):
    @require_auth
    def get(self):
        """Get all payments - Admin only"""
        from flask import session
        if session.get('user_role') != 'admin':
            return {'error': 'Admin access required'}, 403
        
        payments = Payment.query.filter_by(deleted_at=None).all()
        return [{
            'id': p.id,
            'order_id': p.order_id,
            'amount': float(p.amount) if p.amount else 0,
            'status': p.status.value if p.status else None,
            'method': p.method.value if p.method else None,
            'mpesa_transaction_id': p.mpesa_transaction_id,
            'created_at': p.created_at.isoformat() if p.created_at else None
        } for p in payments]
    
    @require_auth
    def post(self):
        """Create new payment - Authenticated users only"""
        data = request.json
        
        payment = Payment(**data)
        db.session.add(payment)
        db.session.commit()
        
        return {
            'message': 'Payment created successfully',
            'payment': {
                'id': payment.id,
                'order_id': payment.order_id,
                'amount': float(payment.amount) if payment.amount else 0,
                'status': payment.status.value if payment.status else None
            }
        }, 201

class PaymentResource(Resource):
    @require_auth
    def get(self, payment_id):
        """Get payment details - Owner or Admin only"""
        payment = Payment.query.get_or_404(payment_id)
        
        # Check if user owns the order
        from flask import session
        if session.get('user_role') != 'admin':
            from app.models import Order
            order = Order.query.get(payment.order_id)
            if order and order.user_id != session.get('user_id'):
                return {'error': 'Access denied'}, 403
        
        return {
            'id': payment.id,
            'order_id': payment.order_id,
            'amount': float(payment.amount) if payment.amount else 0,
            'status': payment.status.value if payment.status else None,
            'method': payment.method.value if payment.method else None,
            'mpesa_transaction_id': payment.mpesa_transaction_id,
            'created_at': payment.created_at.isoformat() if payment.created_at else None
        }
    
    @require_auth
    def put(self, payment_id):
        """Update payment - Owner or Admin only"""
        payment = Payment.query.get_or_404(payment_id)
        
        # Check if user owns the order
        from flask import session
        if session.get('user_role') != 'admin':
            from app.models import Order
            order = Order.query.get(payment.order_id)
            if order and order.user_id != session.get('user_id'):
                return {'error': 'Access denied'}, 403
        
        data = request.json
        
        if 'status' in data:
            payment.status = PaymentStatus(data['status'])
        if 'method' in data:
            payment.method = PaymentMethod(data['method'])
        if 'amount' in data:
            payment.amount = data['amount']
        if 'mpesa_transaction_id' in data:
            payment.mpesa_transaction_id = data['mpesa_transaction_id']
        
        db.session.commit()
        
        return {
            'message': 'Payment updated successfully',
            'payment': {
                'id': payment.id,
                'order_id': payment.order_id,
                'amount': float(payment.amount) if payment.amount else 0,
                'status': payment.status.value if payment.status else None,
                'method': payment.method.value if payment.method else None
            }
        }, 200
    
    @require_auth
    def delete(self, payment_id):
        """Delete payment - Owner or Admin only"""
        payment = Payment.query.get_or_404(payment_id)
        
        # Check if user owns the order
        from flask import session
        if session.get('user_role') != 'admin':
            from app.models import Order
            order = Order.query.get(payment.order_id)
            if order and order.user_id != session.get('user_id'):
                return {'error': 'Access denied'}, 403
        
        from datetime import datetime
        payment.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'message': 'Payment deleted successfully'}, 200

# Register routes
payment_api.add_resource(PaymentListResource, '/')
payment_api.add_resource(PaymentResource, '/<payment_id>')