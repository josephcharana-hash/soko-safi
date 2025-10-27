"""
Review routes for Soko Safi
Handles CRUD operations for reviews
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Review
from app.auth import require_auth, require_role, require_ownership_or_role

review_bp = Blueprint('review_bp', __name__)
review_api = Api(review_bp)

class ReviewListResource(Resource):
    def get(self):
        """Get all reviews - Public access"""
        reviews = Review.query.filter_by(deleted_at=None).all()
        return [{
            'id': r.id,
            'product_id': r.product_id,
            'user_id': r.user_id,
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'updated_at': r.updated_at.isoformat() if r.updated_at else None
        } for r in reviews]
    
    @require_auth
    def post(self):
        """Create new review - Authenticated users only"""
        from flask import session
        data = request.json
        
        # Set user_id to current user if not admin
        if session.get('user_role') != 'admin':
            data['user_id'] = session.get('user_id')
        
        review = Review(**data)
        db.session.add(review)
        db.session.commit()
        
        return {
            'message': 'Review created successfully',
            'review': {
                'id': review.id,
                'product_id': review.product_id,
                'user_id': review.user_id,
                'rating': review.rating,
                'comment': review.comment
            }
        }, 201

class ReviewResource(Resource):
    def get(self, review_id):
        """Get review details - Public access"""
        review = Review.query.get_or_404(review_id)
        return {
            'id': review.id,
            'product_id': review.product_id,
            'user_id': review.user_id,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.isoformat() if review.created_at else None,
            'updated_at': review.updated_at.isoformat() if review.updated_at else None
        }
    
    @require_ownership_or_role('user_id', 'admin')
    def put(self, review_id):
        """Update review - Owner or Admin only"""
        review = Review.query.get_or_404(review_id)
        data = request.json
        
        if 'rating' in data:
            review.rating = data['rating']
        if 'comment' in data:
            review.comment = data['comment']
        if 'user_id' in data and session.get('user_role') == 'admin':
            review.user_id = data['user_id']
        if 'product_id' in data and session.get('user_role') == 'admin':
            review.product_id = data['product_id']
        
        db.session.commit()
        
        return {
            'message': 'Review updated successfully',
            'review': {
                'id': review.id,
                'product_id': review.product_id,
                'user_id': review.user_id,
                'rating': review.rating,
                'comment': review.comment
            }
        }, 200
    
    @require_ownership_or_role('user_id', 'admin')
    def delete(self, review_id):
        """Delete review - Owner or Admin only"""
        review = Review.query.get_or_404(review_id)
        from datetime import datetime
        review.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'message': 'Review deleted successfully'}, 200

# Register routes
review_api.add_resource(ReviewListResource, '/')
review_api.add_resource(ReviewResource, '/<review_id>')