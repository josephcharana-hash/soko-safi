"""
Cart routes for Soko Safi
Handles CRUD operations for carts and cart items
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Cart, CartItem
from app.auth import require_auth, require_role, require_ownership_or_role

cart_bp = Blueprint('cart_bp', __name__)
cart_api = Api(cart_bp)

class CartListResource(Resource):
    @require_auth
    def get(self):
        """Get all carts - Admin only"""
        from flask import session
        if session.get('user_role') != 'admin':
            return {'error': 'Admin access required'}, 403
        
        carts = Cart.query.filter_by(deleted_at=None).all()
        return [{
            'id': c.id,
            'user_id': c.user_id,
            'created_at': c.created_at.isoformat() if c.created_at else None,
            'updated_at': c.updated_at.isoformat() if c.updated_at else None
        } for c in carts]
    
    @require_auth
    def post(self):
        """Create new cart - Authenticated users only"""
        from flask import session
        data = request.json
        
        # Set user_id to current user if not admin
        if session.get('user_role') != 'admin':
            data['user_id'] = session.get('user_id')
        
        cart = Cart(**data)
        db.session.add(cart)
        db.session.commit()
        
        return {
            'message': 'Cart created successfully',
            'cart': {
                'id': cart.id,
                'user_id': cart.user_id
            }
        }, 201

class CartResource(Resource):
    @require_ownership_or_role('user_id', 'admin')
    def get(self, cart_id):
        """Get cart details - Owner or Admin only"""
        cart = Cart.query.get_or_404(cart_id)
        return {
            'id': cart.id,
            'user_id': cart.user_id,
            'created_at': cart.created_at.isoformat() if cart.created_at else None,
            'updated_at': cart.updated_at.isoformat() if cart.updated_at else None
        }
    
    @require_ownership_or_role('user_id', 'admin')
    def put(self, cart_id):
        """Update cart - Owner or Admin only"""
        cart = Cart.query.get_or_404(cart_id)
        data = request.json
        
        # Update allowed fields
        if 'user_id' in data and session.get('user_role') == 'admin':
            cart.user_id = data['user_id']
        
        db.session.commit()
        
        return {
            'message': 'Cart updated successfully',
            'cart': {
                'id': cart.id,
                'user_id': cart.user_id
            }
        }, 200
    
    @require_ownership_or_role('user_id', 'admin')
    def delete(self, cart_id):
        """Delete cart - Owner or Admin only"""
        cart = Cart.query.get_or_404(cart_id)
        from datetime import datetime
        cart.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'message': 'Cart deleted successfully'}, 200

class CartItemListResource(Resource):
    @require_auth
    def get(self):
        """Get user's cart items"""
        from flask import session
        from app.models import Product
        
        current_user_id = session.get('user_id')
        user_role = session.get('user_role')
        
        if user_role == 'admin':
            # Admin gets all cart items
            cart_items = CartItem.query.all()
        else:
            # Regular users get their own cart items
            user_carts = Cart.query.filter_by(user_id=current_user_id).all()
            cart_ids = [c.id for c in user_carts]
            cart_items = CartItem.query.filter(CartItem.cart_id.in_(cart_ids)).all()
        
        # Enhance with product details
        enhanced_items = []
        for ci in cart_items:
            product = Product.query.get(ci.product_id)
            enhanced_items.append({
                'id': ci.id,
                'cart_id': ci.cart_id,
                'product_id': ci.product_id,
                'quantity': ci.quantity,
                'price': float(product.price) if product and product.price else 0,
                'product': {
                    'id': product.id if product else None,
                    'title': product.title if product else 'Unknown Product',
                    'price': float(product.price) if product and product.price else 0,
                    'image': product.image if product else None,
                    'artisan_name': product.artisan_name if product else None
                } if product else None,
                'created_at': ci.added_at.isoformat() if ci.added_at else None
            })
        
        return enhanced_items
    
    @require_auth
    def post(self):
        """Add item to cart - Authenticated users only"""
        from flask import session
        data = request.json
        
        current_user_id = session.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        # Get or create user's cart
        cart = Cart.query.filter_by(user_id=current_user_id).first()
        if not cart:
            cart = Cart(user_id=current_user_id)
            db.session.add(cart)
            db.session.commit()
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            cart_id=cart.id, 
            product_id=product_id
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            db.session.commit()
            cart_item = existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
            db.session.commit()
        
        return {
            'message': 'Item added to cart successfully',
            'cart_item': {
                'id': cart_item.id,
                'cart_id': cart_item.cart_id,
                'product_id': cart_item.product_id,
                'quantity': cart_item.quantity
            }
        }, 201

class CartItemResource(Resource):
    @require_auth
    def get(self, cart_item_id):
        """Get cart item details - Owner or Admin only"""
        cart_item = CartItem.query.get_or_404(cart_item_id)
        
        # Check if user owns the cart
        from flask import session
        if session.get('user_role') != 'admin':
            cart = Cart.query.get(cart_item.cart_id)
            if cart and cart.user_id != session.get('user_id'):
                return {'error': 'Access denied'}, 403
        
        return {
            'id': cart_item.id,
            'cart_id': cart_item.cart_id,
            'product_id': cart_item.product_id,
            'quantity': cart_item.quantity,
            'created_at': cart_item.created_at.isoformat() if cart_item.created_at else None
        }
    
    @require_auth
    def put(self, cart_item_id):
        """Update cart item - Owner or Admin only"""
        cart_item = CartItem.query.get_or_404(cart_item_id)
        
        # Check if user owns the cart
        from flask import session
        if session.get('user_role') != 'admin':
            cart = Cart.query.get(cart_item.cart_id)
            if cart and cart.user_id != session.get('user_id'):
                return {'error': 'Access denied'}, 403
        
        data = request.json
        
        if 'quantity' in data:
            cart_item.quantity = data['quantity']
        if 'product_id' in data:
            cart_item.product_id = data['product_id']
        
        db.session.commit()
        
        return {
            'message': 'Cart item updated successfully',
            'cart_item': {
                'id': cart_item.id,
                'cart_id': cart_item.cart_id,
                'product_id': cart_item.product_id,
                'quantity': cart_item.quantity
            }
        }, 200
    
    @require_auth
    def delete(self, cart_item_id):
        """Delete cart item - Owner or Admin only"""
        cart_item = CartItem.query.get_or_404(cart_item_id)
        
        # Check if user owns the cart
        from flask import session
        if session.get('user_role') != 'admin':
            cart = Cart.query.get(cart_item.cart_id)
            if cart and cart.user_id != session.get('user_id'):
                return {'error': 'Access denied'}, 403
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return {'message': 'Cart item deleted successfully'}, 200

class ClearCartResource(Resource):
    @require_auth
    def delete(self):
        """Clear user's cart"""
        from flask import session
        current_user_id = session.get('user_id')
        
        # Get user's cart
        cart = Cart.query.filter_by(user_id=current_user_id).first()
        if cart:
            # Delete all cart items
            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            for item in cart_items:
                db.session.delete(item)
            db.session.commit()
        
        return {'message': 'Cart cleared successfully'}, 200

# Register routes
cart_api.add_resource(CartItemListResource, '/')
cart_api.add_resource(CartItemResource, '/<cart_item_id>')
cart_api.add_resource(ClearCartResource, '/clear')