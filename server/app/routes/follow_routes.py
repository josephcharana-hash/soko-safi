"""
Follow routes for Soko Safi
Handles CRUD operations for follows
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Follow
from app.auth import require_auth, require_role, require_ownership_or_role

follow_bp = Blueprint('follow_bp', __name__)
follow_api = Api(follow_bp)

class FollowListResource(Resource):
    @require_auth
    def get(self):
        """Get all follows - Admin only"""
        from flask import session
        if session.get('user_role') != 'admin':
            return {'error': 'Admin access required'}, 403
        
        follows = Follow.query.filter_by(deleted_at=None).all()
        return [{
            'id': f.id,
            'follower_id': f.follower_id,
            'following_id': f.following_id,
            'created_at': f.created_at.isoformat() if f.created_at else None
        } for f in follows]
    
    @require_auth
    def post(self):
        """Create new follow - Authenticated users only"""
        from flask import session
        data = request.json
        
        # Set follower_id to current user if not admin
        if session.get('user_role') != 'admin':
            data['follower_id'] = session.get('user_id')
        
        follow = Follow(**data)
        db.session.add(follow)
        db.session.commit()
        
        return {
            'message': 'Follow created successfully',
            'follow': {
                'id': follow.id,
                'follower_id': follow.follower_id,
                'following_id': follow.following_id
            }
        }, 201

class FollowResource(Resource):
    @require_ownership_or_role('follower_id', 'admin')
    def get(self, follow_id):
        """Get follow details - Owner or Admin only"""
        follow = Follow.query.get_or_404(follow_id)
        return {
            'id': follow.id,
            'follower_id': follow.follower_id,
            'following_id': follow.following_id,
            'created_at': follow.created_at.isoformat() if follow.created_at else None
        }
    
    @require_ownership_or_role('follower_id', 'admin')
    def put(self, follow_id):
        """Update follow - Owner or Admin only"""
        follow = Follow.query.get_or_404(follow_id)
        data = request.json
        
        if 'following_id' in data:
            follow.following_id = data['following_id']
        if 'follower_id' in data and session.get('user_role') == 'admin':
            follow.follower_id = data['follower_id']
        
        db.session.commit()
        
        return {
            'message': 'Follow updated successfully',
            'follow': {
                'id': follow.id,
                'follower_id': follow.follower_id,
                'following_id': follow.following_id
            }
        }, 200
    
    @require_ownership_or_role('follower_id', 'admin')
    def delete(self, follow_id):
        """Delete follow - Owner or Admin only"""
        follow = Follow.query.get_or_404(follow_id)
        from datetime import datetime
        follow.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'message': 'Follow deleted successfully'}, 200

# Register routes
follow_api.add_resource(FollowListResource, '/')
follow_api.add_resource(FollowResource, '/<follow_id>')
