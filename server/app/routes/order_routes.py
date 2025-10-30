"""
Order routes for Soko Safi
Handles CRUD operations for orders and order items
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Order, OrderItem, OrderStatus
from app.auth import require_auth, require_role, require_ownership_or_role

order_bp = Blueprint('order_bp', __name__)
order_api = Api(order_bp)

class OrderListResource(Resource):
    @require_auth
    def get(self):
        """Get orders - Admin gets all, users get their own orders"""
        from flask import session
        from app.models import User, OrderItem, Product

        current_user_id = session.get('user_id')
        user_role = session.get('user_role')

        if user_role == 'admin':
            # Admin gets all orders
            orders = Order.query.filter_by(deleted_at=None).all()
        else:
            # Regular users get their own orders
            orders = Order.query.filter_by(user_id=current_user_id, deleted_at=None).all()

        # Enhance orders with additional data
        enhanced_orders = []
        for order in orders:
            # Get order items with product details
            order_items = db.session.query(OrderItem, Product).join(
                Product, OrderItem.product_id == Product.id
            ).filter(OrderItem.order_id == order.id, OrderItem.deleted_at.is_(None)).all()

            # Get user details for the order
            user = User.query.get(order.user_id) if order.user_id else None

            enhanced_order = {
                'id': order.id,
                'user_id': order.user_id,
                'user_name': user.full_name if user else 'Unknown User',
                'user_email': user.email if user else '',
                'status': order.status.value if order.status else 'pending',
                'total_amount': float(order.total_amount) if order.total_amount else 0,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'updated_at': order.updated_at.isoformat() if order.updated_at else None,
                'items': [{
                    'product_id': item.product_id,
                    'product_title': product.title if product else 'Unknown Product',
                    'quantity': item.quantity,
                    'unit_price': float(item.unit_price) if item.unit_price else 0,
                    'total_price': float(item.total_price) if item.total_price else 0,
                    'artisan_id': item.artisan_id
                } for item, product in order_items]
            }
            enhanced_orders.append(enhanced_order)

        return enhanced_orders
    
    @require_auth
    def post(self):
        """Create new order - Authenticated users only"""
        from flask import session
        data = request.json
        
        if not data:
            return {'error': 'No data provided'}, 400
        
        try:
            # Set user_id to current user if not admin
            user_id = session.get('user_id')
            if session.get('user_role') == 'admin' and 'user_id' in data:
                user_id = data['user_id']
            
            order = Order(
                user_id=user_id,
                status=OrderStatus(data.get('status', 'pending')),
                total_amount=data.get('total_amount', 0)
            )
            db.session.add(order)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create order'}, 500
        
        return {
            'message': 'Order created successfully',
            'order': {
                'id': order.id,
                'user_id': order.user_id,
                'status': order.status.value if order.status else None
            }
        }, 201

class OrderResource(Resource):
    @require_ownership_or_role('user_id', 'admin')
    def get(self, order_id):
        """Get order details - Owner or Admin only"""
        order = Order.query.get_or_404(order_id)
        return {
            'id': order.id,
            'user_id': order.user_id,
            'status': order.status.value if order.status else None,
            'total_amount': float(order.total_amount) if order.total_amount else 0,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'updated_at': order.updated_at.isoformat() if order.updated_at else None
        }
    
    @require_ownership_or_role('user_id', 'admin')
    def put(self, order_id):
        """Update order - Owner or Admin only"""
        try:
            order = Order.query.get_or_404(order_id)
            data = request.json
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            from flask import session
            # Update allowed fields
            if 'status' in data:
                order.status = OrderStatus(data['status'])
            if 'total_amount' in data:
                order.total_amount = data['total_amount']
            if 'user_id' in data and session.get('user_role') == 'admin':
                order.user_id = data['user_id']
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to update order'}, 500
        
        return {
            'message': 'Order updated successfully',
            'order': {
                'id': order.id,
                'user_id': order.user_id,
                'status': order.status.value if order.status else None,
                'total_amount': float(order.total_amount) if order.total_amount else 0
            }
        }, 200
    
    @require_ownership_or_role('user_id', 'admin')
    def delete(self, order_id):
        """Delete order - Owner or Admin only"""
        try:
            order = Order.query.get_or_404(order_id)
            from datetime import datetime
            order.deleted_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to delete order'}, 500
        
        return {'message': 'Order deleted successfully'}, 200

class OrderItemListResource(Resource):
    @require_auth
    def get(self):
        """Get all order items - Admin only"""
        from flask import session
        if session.get('user_role') != 'admin':
            return {'error': 'Admin access required'}, 403
        
        order_items = OrderItem.query.filter_by(deleted_at=None).all()
        return [{
            'id': oi.id,
            'order_id': oi.order_id,
            'product_id': oi.product_id,
            'artisan_id': oi.artisan_id,
            'quantity': oi.quantity,
            'unit_price': float(oi.unit_price) if oi.unit_price else 0,
            'total_price': float(oi.total_price) if oi.total_price else 0,
            'created_at': oi.created_at.isoformat() if oi.created_at else None
        } for oi in order_items]
    
    @require_auth
    def post(self):
        """Create new order item - Authenticated users only"""
        data = request.json
        
        if not data or not all(k in data for k in ['order_id', 'product_id', 'quantity']):
            return {'error': 'order_id, product_id, and quantity are required'}, 400
        
        try:
            order_item = OrderItem(
                order_id=data.get('order_id'),
                product_id=data.get('product_id'),
                artisan_id=data.get('artisan_id'),
                quantity=data.get('quantity'),
                unit_price=data.get('unit_price', 0),
                total_price=data.get('total_price', 0)
            )
            db.session.add(order_item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create order item'}, 500
        
        return {
            'message': 'Order item created successfully',
            'order_item': {
                'id': order_item.id,
                'order_id': order_item.order_id,
                'product_id': order_item.product_id,
                'artisan_id': order_item.artisan_id,
                'quantity': order_item.quantity
            }
        }, 201

class OrderItemResource(Resource):
    @require_auth
    def get(self, order_item_id):
        """Get order item details - Owner or Admin only"""
        try:
            order_item = OrderItem.query.get_or_404(order_item_id)
            
            # Check if user owns the order
            from flask import session
            if session.get('user_role') != 'admin':
                order = Order.query.get(order_item.order_id)
                if order and order.user_id != session.get('user_id'):
                    return {'error': 'Access denied'}, 403
        except Exception as e:
            return {'error': 'Order item not found'}, 404
        
        return {
            'id': order_item.id,
            'order_id': order_item.order_id,
            'product_id': order_item.product_id,
            'artisan_id': order_item.artisan_id,
            'quantity': order_item.quantity,
            'unit_price': float(order_item.unit_price) if order_item.unit_price else 0,
            'total_price': float(order_item.total_price) if order_item.total_price else 0,
            'created_at': order_item.created_at.isoformat() if order_item.created_at else None
        }
    
    @require_auth
    def put(self, order_item_id):
        """Update order item - Owner or Admin only"""
        try:
            order_item = OrderItem.query.get_or_404(order_item_id)
            
            # Check if user owns the order
            from flask import session
            if session.get('user_role') != 'admin':
                order = Order.query.get(order_item.order_id)
                if order and order.user_id != session.get('user_id'):
                    return {'error': 'Access denied'}, 403
            
            data = request.json
            if not data:
                return {'error': 'No data provided'}, 400
            
            if 'quantity' in data:
                order_item.quantity = data['quantity']
            if 'unit_price' in data:
                order_item.unit_price = data['unit_price']
            if 'total_price' in data:
                order_item.total_price = data['total_price']
            if 'product_id' in data:
                order_item.product_id = data['product_id']
            if 'artisan_id' in data:
                order_item.artisan_id = data['artisan_id']
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to update order item'}, 500
        
        return {
            'message': 'Order item updated successfully',
            'order_item': {
                'id': order_item.id,
                'order_id': order_item.order_id,
                'product_id': order_item.product_id,
                'artisan_id': order_item.artisan_id,
                'quantity': order_item.quantity
            }
        }, 200
    
    @require_auth
    def delete(self, order_item_id):
        """Delete order item - Owner or Admin only"""
        try:
            order_item = OrderItem.query.get_or_404(order_item_id)
            
            # Check if user owns the order
            from flask import session
            if session.get('user_role') != 'admin':
                order = Order.query.get(order_item.order_id)
                if order and order.user_id != session.get('user_id'):
                    return {'error': 'Access denied'}, 403
            
            from datetime import datetime
            order_item.deleted_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to delete order item'}, 500
        
        return {'message': 'Order item deleted successfully'}, 200

# Register routes
order_api.add_resource(OrderListResource, '/')
order_api.add_resource(OrderResource, '/<order_id>')
order_api.add_resource(OrderItemListResource, '/items/')
order_api.add_resource(OrderItemResource, '/items/<order_item_id>')