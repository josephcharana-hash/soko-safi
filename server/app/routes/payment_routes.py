"""
Payment routes for Soko Safi
Handles CRUD operations for payments and M-Pesa integration
"""

from flask_restful import Resource, Api
from flask import Blueprint, request, jsonify
from app.models import db, Payment, PaymentMethod, PaymentStatus, Order, OrderItem, User, ArtisanDisbursement
from app.auth import require_auth, require_role, require_ownership_or_role
from app.services.mpesa_service import mpesa_service

payment_bp = Blueprint('payment_bp', __name__)
payment_api = Api(payment_bp)

class PaymentListResource(Resource):
    @require_auth
    def get(self):
        """Get payments - Admin gets all, users get their own payments"""
        from flask import session
        from app.models import Order

        current_user_id = session.get('user_id')
        user_role = session.get('user_role')

        if user_role == 'admin':
            # Admin gets all payments
            payments = Payment.query.filter_by(deleted_at=None).all()
        else:
            # Regular users get payments for their orders
            user_order_ids = [o.id for o in Order.query.filter_by(user_id=current_user_id).all()]
            payments = Payment.query.filter(Payment.order_id.in_(user_order_ids), Payment.deleted_at.is_(None)).all()

        # Enhance payments with order details
        enhanced_payments = []
        for payment in payments:
            order = Order.query.get(payment.order_id) if payment.order_id else None

            enhanced_payment = {
                'id': payment.id,
                'order_id': payment.order_id,
                'amount': float(payment.amount) if payment.amount else 0,
                'status': payment.status.value if payment.status else 'pending',
                'method': payment.method.value if payment.method else 'mpesa',
                'mpesa_transaction_id': payment.mpesa_transaction_id,
                'created_at': payment.created_at.isoformat() if payment.created_at else None,
                'updated_at': payment.updated_at.isoformat() if payment.updated_at else None,
                'order_date': order.created_at.isoformat() if order and order.created_at else None
            }
            enhanced_payments.append(enhanced_payment)

        return enhanced_payments
    
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

class InitiatePaymentResource(Resource):
    @require_auth
    def post(self):
        """Initiate M-Pesa payment for an order"""
        data = request.json
        order_id = data.get('order_id')
        phone_number = data.get('phone_number')

        if not order_id or not phone_number:
            return {'error': 'Order ID and phone number are required'}, 400

        try:
            # Get order and calculate total
            order = Order.query.get_or_404(order_id)

            # Check if user owns the order
            from flask import session
            if order.user_id != session.get('user_id'):
                return {'error': 'Access denied'}, 403

            # Calculate order total
            total_amount = sum(float(item.total_price) for item in order.order_items)

            # Create payment record
            payment = Payment(
                order_id=order_id,
                amount=total_amount,
                currency='KES',
                payer_phone=phone_number,
                status=PaymentStatus.pending
            )
            db.session.add(payment)
            db.session.commit()

            # Initiate STK Push
            result = mpesa_service.initiate_stk_push(
                phone_number=phone_number,
                amount=total_amount,
                order_id=order_id,
                account_reference=f"Order-{order_id}"
            )

            if result['success']:
                # Store checkout request ID for callback matching
                payment.mpesa_transaction_id = result['checkout_request_id']
                db.session.commit()

                return {
                    'message': 'Payment initiated successfully',
                    'payment_id': payment.id,
                    'checkout_request_id': result['checkout_request_id'],
                    'customer_message': result['customer_message']
                }, 200
            else:
                payment.status = PaymentStatus.failed
                payment.transaction_status_reason = result.get('error', 'STK Push failed')
                db.session.commit()

                return {
                    'error': 'Failed to initiate payment',
                    'details': result.get('error')
                }, 500

        except Exception as e:
            db.session.rollback()
            return {'error': f'Payment initiation failed: {str(e)}'}, 500


class PaymentStatusResource(Resource):
    @require_auth
    def get(self, payment_id):
        """Get payment status"""
        try:
            payment = Payment.query.get_or_404(payment_id)

            # Check ownership
            from flask import session
            order = Order.query.get(payment.order_id)
            if order and order.user_id != session.get('user_id') and session.get('user_role') != 'admin':
                return {'error': 'Access denied'}, 403

            # Get disbursements for this payment
            disbursements = ArtisanDisbursement.query.filter_by(payment_id=payment_id).all()

            return {
                'payment': {
                    'id': payment.id,
                    'order_id': payment.order_id,
                    'amount': float(payment.amount),
                    'status': payment.status.value,
                    'mpesa_transaction_id': payment.mpesa_transaction_id,
                    'created_at': payment.created_at.isoformat()
                },
                'disbursements': [{
                    'id': d.id,
                    'artisan_id': d.artisan_id,
                    'amount': float(d.amount),
                    'status': d.status.value,
                    'method': d.disbursement_method,
                    'retry_count': d.retry_count,
                    'failure_reason': d.failure_reason
                } for d in disbursements]
            }, 200

        except Exception as e:
            return {'error': f'Failed to get payment status: {str(e)}'}, 500


class PaymentCallbackResource(Resource):
    def post(self):
        """Handle M-Pesa STK Push callback"""
        try:
            callback_data = request.json
            mpesa_service.process_stk_callback(callback_data)
            return {'message': 'Callback processed successfully'}, 200
        except Exception as e:
            current_app.logger.error(f"Callback processing error: {str(e)}")
            return {'error': 'Callback processing failed'}, 500


class B2CResultResource(Resource):
    def post(self):
        """Handle M-Pesa B2C result callback"""
        try:
            result_data = request.json
            mpesa_service.process_b2c_result(result_data)
            return {'message': 'B2C result processed successfully'}, 200
        except Exception as e:
            current_app.logger.error(f"B2C result processing error: {str(e)}")
            return {'error': 'B2C result processing failed'}, 500


class B2CTimeoutResource(Resource):
    def post(self):
        """Handle M-Pesa B2C timeout"""
        try:
            timeout_data = request.json
            # Handle timeout - mark as failed and retry
            conversation_id = timeout_data.get('Result', {}).get('ConversationId')
            if conversation_id:
                # Find disbursement and mark for retry
                disbursement = ArtisanDisbursement.query.filter_by(mpesa_transaction_id=conversation_id).first()
                if disbursement:
                    disbursement.status = DisbursementStatus.retry
                    disbursement.failure_reason = 'B2C Timeout'
                    db.session.commit()

            return {'message': 'B2C timeout handled'}, 200
        except Exception as e:
            current_app.logger.error(f"B2C timeout handling error: {str(e)}")
            return {'error': 'B2C timeout handling failed'}, 500


# Register routes
payment_api.add_resource(PaymentListResource, '/')
payment_api.add_resource(PaymentResource, '/<payment_id>')
payment_api.add_resource(InitiatePaymentResource, '/initiate')
payment_api.add_resource(PaymentStatusResource, '/status/<payment_id>')
payment_api.add_resource(PaymentCallbackResource, '/callback')
payment_api.add_resource(B2CResultResource, '/b2c/result')
payment_api.add_resource(B2CTimeoutResource, '/b2c/timeout')