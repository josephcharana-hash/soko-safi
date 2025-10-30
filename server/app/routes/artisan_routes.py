"""
Artisan routes for Soko Safi
Handles CRUD operations for artisan showcase media and social links
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, ArtisanShowcaseMedia, ArtisanSocial
from app.auth import require_auth, require_role, require_ownership_or_role

artisan_bp = Blueprint('artisan_bp', __name__)
artisan_api = Api(artisan_bp)

class ArtisanShowcaseMediaListResource(Resource):
    @require_auth
    def get(self):
        """Get all artisan showcase media - Admin only"""
        from flask import session
        if session.get('user_role') != 'admin':
            return {'error': 'Admin access required'}, 403
        
        showcase_media = ArtisanShowcaseMedia.query.filter_by(deleted_at=None).all()
        return [{
            'id': sm.id,
            'artisan_id': sm.artisan_id,
            'media_type': sm.media_type,
            'media_url': sm.media_url,
            'caption': sm.caption,
            'created_at': sm.created_at.isoformat() if sm.created_at else None
        } for sm in showcase_media]
    
    @require_role('artisan', 'admin')
    def post(self):
        """Create new artisan showcase media - Artisan or Admin only"""
        from flask import session
        data = request.json
        
        if not data or 'media_type' not in data or 'media_url' not in data:
            return {'error': 'media_type and media_url are required'}, 400
        
        try:
            # Set artisan_id to current user if not admin
            artisan_id = session.get('user_id')
            if session.get('user_role') == 'admin' and 'artisan_id' in data:
                artisan_id = data['artisan_id']
            
            showcase_media = ArtisanShowcaseMedia(
                artisan_id=artisan_id,
                media_type=data.get('media_type'),
                media_url=data.get('media_url'),
                caption=data.get('caption')
            )
            db.session.add(showcase_media)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create showcase media'}, 500
        
        return {
            'message': 'Artisan showcase media created successfully',
            'showcase_media': {
                'id': showcase_media.id,
                'artisan_id': showcase_media.artisan_id,
                'media_type': showcase_media.media_type,
                'media_url': showcase_media.media_url,
                'caption': showcase_media.caption
            }
        }, 201

class ArtisanShowcaseMediaResource(Resource):
    @require_ownership_or_role('artisan_id', 'admin')
    def get(self, showcase_media_id):
        """Get artisan showcase media details - Owner or Admin only"""
        showcase_media = ArtisanShowcaseMedia.query.get_or_404(showcase_media_id)
        return {
            'id': showcase_media.id,
            'artisan_id': showcase_media.artisan_id,
            'media_type': showcase_media.media_type,
            'media_url': showcase_media.media_url,
            'caption': showcase_media.caption,
            'created_at': showcase_media.created_at.isoformat() if showcase_media.created_at else None
        }
    
    @require_ownership_or_role('artisan_id', 'admin')
    def put(self, showcase_media_id):
        """Update artisan showcase media - Owner or Admin only"""
        try:
            showcase_media = ArtisanShowcaseMedia.query.get_or_404(showcase_media_id)
            data = request.json
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            from flask import session
            if 'media_type' in data:
                showcase_media.media_type = data['media_type']
            if 'media_url' in data:
                showcase_media.media_url = data['media_url']
            if 'caption' in data:
                showcase_media.caption = data['caption']
            if 'artisan_id' in data and session.get('user_role') == 'admin':
                showcase_media.artisan_id = data['artisan_id']
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to update showcase media'}, 500
        
        return {
            'message': 'Artisan showcase media updated successfully',
            'showcase_media': {
                'id': showcase_media.id,
                'artisan_id': showcase_media.artisan_id,
                'media_type': showcase_media.media_type,
                'media_url': showcase_media.media_url,
                'caption': showcase_media.caption
            }
        }, 200
    
    @require_ownership_or_role('artisan_id', 'admin')
    def delete(self, showcase_media_id):
        """Delete artisan showcase media - Owner or Admin only"""
        try:
            showcase_media = ArtisanShowcaseMedia.query.get_or_404(showcase_media_id)
            from datetime import datetime
            showcase_media.deleted_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to delete showcase media'}, 500
        
        return {'message': 'Artisan showcase media deleted successfully'}, 200

class ArtisanSocialListResource(Resource):
    @require_auth
    def get(self):
        """Get all artisan social links - Admin only"""
        from flask import session
        if session.get('user_role') != 'admin':
            return {'error': 'Admin access required'}, 403
        
        social_links = ArtisanSocial.query.filter_by(deleted_at=None).all()
        return [{
            'id': asl.id,
            'artisan_id': asl.artisan_id,
            'platform': asl.platform,
            'url': asl.url,
            'created_at': asl.created_at.isoformat() if asl.created_at else None
        } for asl in social_links]
    
    @require_role('artisan', 'admin')
    def post(self):
        """Create new artisan social link - Artisan or Admin only"""
        from flask import session
        data = request.json
        
        if not data or 'platform' not in data or 'url' not in data:
            return {'error': 'platform and url are required'}, 400
        
        try:
            # Set artisan_id to current user if not admin
            artisan_id = session.get('user_id')
            if session.get('user_role') == 'admin' and 'artisan_id' in data:
                artisan_id = data['artisan_id']
            
            social_link = ArtisanSocial(
                artisan_id=artisan_id,
                platform=data.get('platform'),
                url=data.get('url')
            )
            db.session.add(social_link)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create social link'}, 500
        
        return {
            'message': 'Artisan social link created successfully',
            'social_link': {
                'id': social_link.id,
                'artisan_id': social_link.artisan_id,
                'platform': social_link.platform,
                'url': social_link.url
            }
        }, 201

class ArtisanSocialResource(Resource):
    @require_ownership_or_role('artisan_id', 'admin')
    def get(self, social_link_id):
        """Get artisan social link details - Owner or Admin only"""
        social_link = ArtisanSocial.query.get_or_404(social_link_id)
        return {
            'id': social_link.id,
            'artisan_id': social_link.artisan_id,
            'platform': social_link.platform,
            'url': social_link.url,
            'created_at': social_link.created_at.isoformat() if social_link.created_at else None
        }
    
    @require_ownership_or_role('artisan_id', 'admin')
    def put(self, social_link_id):
        """Update artisan social link - Owner or Admin only"""
        social_link = ArtisanSocial.query.get_or_404(social_link_id)
        data = request.json
        
        if 'platform' in data:
            social_link.platform = data['platform']
        if 'url' in data:
            social_link.url = data['url']
        if 'artisan_id' in data and session.get('user_role') == 'admin':
            social_link.artisan_id = data['artisan_id']
        
        db.session.commit()
        
        return {
            'message': 'Artisan social link updated successfully',
            'social_link': {
                'id': social_link.id,
                'artisan_id': social_link.artisan_id,
                'platform': social_link.platform,
                'url': social_link.url
            }
        }, 200
    
    @require_ownership_or_role('artisan_id', 'admin')
    def delete(self, social_link_id):
        """Delete artisan social link - Owner or Admin only"""
        social_link = ArtisanSocial.query.get_or_404(social_link_id)
        from datetime import datetime
        social_link.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'message': 'Artisan social link deleted successfully'}, 200

class ArtisanDashboardResource(Resource):
    @require_role('artisan', 'admin')
    def get(self):
        """Get artisan dashboard statistics - Artisan or Admin only"""
        from flask import session
        from app.models import Product, Order, OrderItem, Message
        from sqlalchemy import func, and_

        current_user_id = session.get('user_id')

        # Get product count for this artisan
        product_count = Product.query.filter_by(artisan_id=current_user_id, deleted_at=None).count()

        # Get order count for this artisan (orders containing their products)
        order_count = db.session.query(func.count(func.distinct(Order.id))).join(OrderItem, Order.id == OrderItem.order_id).filter(
            and_(OrderItem.artisan_id == current_user_id, Order.deleted_at.is_(None))
        ).scalar()

        # Get total revenue for this artisan
        revenue_result = db.session.query(func.sum(OrderItem.total_price)).join(Order, Order.id == OrderItem.order_id).filter(
            and_(OrderItem.artisan_id == current_user_id, Order.status == 'completed', Order.deleted_at.is_(None))
        ).scalar()
        total_revenue = float(revenue_result) if revenue_result else 0.0

        # Get recent orders for this artisan
        recent_orders = db.session.query(Order, OrderItem).join(OrderItem, Order.id == OrderItem.order_id).filter(
            and_(OrderItem.artisan_id == current_user_id, Order.deleted_at.is_(None))
        ).order_by(Order.created_at.desc()).limit(5).all()

        # Get recent messages for this artisan
        recent_messages = Message.query.filter(
            and_(
                Message.receiver_id == current_user_id,
                Message.deleted_at.is_(None)
            )
        ).order_by(Message.timestamp.desc()).limit(5).all()

        return {
            'stats': {
                'total_products': product_count,
                'total_orders': order_count,
                'total_revenue': total_revenue
            },
            'recent_orders': [{
                'id': order.id,
                'status': order.status.value if order.status else 'pending',
                'total_amount': float(order.total_amount) if order.total_amount else 0,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'product_title': order_item.product.title if hasattr(order_item, 'product') and order_item.product else 'Unknown Product'
            } for order, order_item in recent_orders],
            'recent_messages': [{
                'id': msg.id,
                'sender_id': msg.sender_id,
                'message': msg.message,
                'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
                'is_read': msg.is_read
            } for msg in recent_messages]
        }

class ArtisanOrdersResource(Resource):
    @require_role('artisan', 'admin')
    def get(self):
        """Get orders for artisan's products - Artisan or Admin only"""
        from flask import session
        from app.models import Order, OrderItem, User
        from sqlalchemy import and_

        current_user_id = session.get('user_id')

        # Get all orders containing this artisan's products
        orders = db.session.query(Order, OrderItem, User).join(OrderItem, Order.id == OrderItem.order_id).join(
            User, Order.user_id == User.id
        ).filter(
            and_(OrderItem.artisan_id == current_user_id, Order.deleted_at.is_(None))
        ).order_by(Order.created_at.desc()).all()

        # Group by order to avoid duplicates
        order_dict = {}
        for order, order_item, user in orders:
            if order.id not in order_dict:
                order_dict[order.id] = {
                    'id': order.id,
                    'user_id': order.user_id,
                    'user_name': user.full_name or 'Unknown User',
                    'user_email': user.email,
                    'status': order.status.value if order.status else 'pending',
                    'total_amount': float(order.total_amount) if order.total_amount else 0,
                    'created_at': order.created_at.isoformat() if order.created_at else None,
                    'updated_at': order.updated_at.isoformat() if order.updated_at else None,
                    'items': []
                }
            order_dict[order.id]['items'].append({
                'product_id': order_item.product_id,
                'product_title': order_item.product.title if hasattr(order_item, 'product') and order_item.product else 'Unknown Product',
                'quantity': order_item.quantity,
                'unit_price': float(order_item.unit_price) if order_item.unit_price else 0,
                'total_price': float(order_item.total_price) if order_item.total_price else 0
            })

        return list(order_dict.values())

class ArtisanMessagesResource(Resource):
    @require_role('artisan', 'admin')
    def get(self):
        """Get messages for artisan - Artisan or Admin only"""
        from flask import session
        from app.models import Message, User

        current_user_id = session.get('user_id')

        # Get all messages where artisan is receiver
        messages = db.session.query(Message, User).join(
            User, Message.sender_id == User.id
        ).filter(
            and_(Message.receiver_id == current_user_id, Message.deleted_at.is_(None))
        ).order_by(Message.timestamp.desc()).all()

        return [{
            'id': msg.id,
            'sender_id': msg.sender_id,
            'sender_name': user.full_name or 'Unknown User',
            'sender_email': user.email,
            'message': msg.message,
            'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
            'is_read': msg.is_read
        } for msg, user in messages]

class ArtisanProductsResource(Resource):
    def get(self, artisan_id):
        """Get products by artisan ID - Public access"""
        from app.models import Product
        
        products = Product.query.filter_by(artisan_id=artisan_id, deleted_at=None).all()
        
        return [{
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'price': float(product.price) if product.price else 0,
            'currency': product.currency or 'KSH',
            'stock': product.stock or 0,
            'image': product.image,
            'category': product.category.name if product.category else None,
            'subcategory': product.subcategory.name if product.subcategory else None,
            'status': product.status,
            'created_at': product.created_at.isoformat() if product.created_at else None
        } for product in products]

# Register routes
artisan_api.add_resource(ArtisanShowcaseMediaListResource, '/showcase/')
artisan_api.add_resource(ArtisanShowcaseMediaResource, '/showcase/<showcase_media_id>')
artisan_api.add_resource(ArtisanSocialListResource, '/social/')
artisan_api.add_resource(ArtisanSocialResource, '/social/<social_link_id>')
artisan_api.add_resource(ArtisanDashboardResource, '/dashboard')
artisan_api.add_resource(ArtisanOrdersResource, '/orders')
artisan_api.add_resource(ArtisanMessagesResource, '/messages')
artisan_api.add_resource(ArtisanProductsResource, '/<artisan_id>/products')
