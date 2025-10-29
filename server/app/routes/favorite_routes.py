"""
Favorite routes for Soko Safi
Handles CRUD operations for favorites
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Favorite
from app.auth import require_auth, require_role, require_ownership_or_role

favorite_bp = Blueprint('favorite_bp', __name__)
favorite_api = Api(favorite_bp)

class FavoriteListResource(Resource):
    @require_auth
    def get(self):
        """Get favorites - Admin gets all, users get their own favorites"""
        from flask import session
        from app.models import Product

        current_user_id = session.get('user_id')
        user_role = session.get('user_role')

        if user_role == 'admin':
            # Admin gets all favorites
            favorites = Favorite.query.filter_by(deleted_at=None).all()
        else:
            # Regular users get their own favorites
            favorites = Favorite.query.filter_by(user_id=current_user_id, deleted_at=None).all()

        # Enhance favorites with product details
        enhanced_favorites = []
        for favorite in favorites:
            product = Product.query.get(favorite.product_id) if favorite.product_id else None

            enhanced_favorite = {
                'id': favorite.id,
                'user_id': favorite.user_id,
                'product_id': favorite.product_id,
                'product': {
                    'id': product.id if product else None,
                    'title': product.title if product else 'Unknown Product',
                    'price': float(product.price) if product and product.price else 0,
                    'image': product.image if product else None,
                    'artisan_name': product.artisan_name if product else None
                } if product else None,
                'created_at': favorite.created_at.isoformat() if favorite.created_at else None
            }
            enhanced_favorites.append(enhanced_favorite)

        return enhanced_favorites
    
    @require_auth
    def post(self):
        """Create new favorite - Authenticated users only"""
        from flask import session
        data = request.json
        
        if not data or 'product_id' not in data:
            return {'error': 'product_id is required'}, 400
        
        try:
            # Set user_id to current user if not admin
            user_id = session.get('user_id')
            if session.get('user_role') == 'admin' and 'user_id' in data:
                user_id = data['user_id']
            
            # Check if favorite already exists
            existing = Favorite.query.filter_by(
                user_id=user_id, 
                product_id=data['product_id'],
                deleted_at=None
            ).first()
            
            if existing:
                return {'error': 'Product already in favorites'}, 409
            
            favorite = Favorite(
                user_id=user_id,
                product_id=data['product_id']
            )
            db.session.add(favorite)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create favorite'}, 500
        
        return {
            'message': 'Favorite created successfully',
            'favorite': {
                'id': favorite.id,
                'user_id': favorite.user_id,
                'product_id': favorite.product_id
            }
        }, 201

class FavoriteResource(Resource):
    @require_ownership_or_role('user_id', 'admin')
    def get(self, favorite_id):
        """Get favorite details - Owner or Admin only"""
        favorite = Favorite.query.get_or_404(favorite_id)
        return {
            'id': favorite.id,
            'user_id': favorite.user_id,
            'product_id': favorite.product_id,
            'created_at': favorite.created_at.isoformat() if favorite.created_at else None
        }
    
    @require_ownership_or_role('user_id', 'admin')
    def put(self, favorite_id):
        """Update favorite - Owner or Admin only"""
        favorite = Favorite.query.get_or_404(favorite_id)
        data = request.json
        
        if not data:
            return {'error': 'No data provided'}, 400
        
        try:
            from flask import session
            if 'product_id' in data:
                favorite.product_id = data['product_id']
            if 'user_id' in data and session.get('user_role') == 'admin':
                favorite.user_id = data['user_id']
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to update favorite'}, 500
        
        return {
            'message': 'Favorite updated successfully',
            'favorite': {
                'id': favorite.id,
                'user_id': favorite.user_id,
                'product_id': favorite.product_id
            }
        }, 200
    
    @require_ownership_or_role('user_id', 'admin')
    def delete(self, favorite_id):
        """Delete favorite - Owner or Admin only"""
        favorite = Favorite.query.get_or_404(favorite_id)
        
        try:
            from datetime import datetime
            favorite.deleted_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to delete favorite'}, 500
        
        return {'message': 'Favorite deleted successfully'}, 200

# Register routes
favorite_api.add_resource(FavoriteListResource, '/')
favorite_api.add_resource(FavoriteResource, '/<favorite_id>')
