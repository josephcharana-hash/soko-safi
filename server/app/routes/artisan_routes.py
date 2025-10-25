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
        
        # Set artisan_id to current user if not admin
        if session.get('user_role') != 'admin':
            data['artisan_id'] = session.get('user_id')
        
        showcase_media = ArtisanShowcaseMedia(**data)
        db.session.add(showcase_media)
        db.session.commit()
        
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
        showcase_media = ArtisanShowcaseMedia.query.get_or_404(showcase_media_id)
        data = request.json
        
        if 'media_type' in data:
            showcase_media.media_type = data['media_type']
        if 'media_url' in data:
            showcase_media.media_url = data['media_url']
        if 'caption' in data:
            showcase_media.caption = data['caption']
        if 'artisan_id' in data and session.get('user_role') == 'admin':
            showcase_media.artisan_id = data['artisan_id']
        
        db.session.commit()
        
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
        showcase_media = ArtisanShowcaseMedia.query.get_or_404(showcase_media_id)
        from datetime import datetime
        showcase_media.deleted_at = datetime.utcnow()
        db.session.commit()
        
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
        
        # Set artisan_id to current user if not admin
        if session.get('user_role') != 'admin':
            data['artisan_id'] = session.get('user_id')
        
        social_link = ArtisanSocial(**data)
        db.session.add(social_link)
        db.session.commit()
        
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

# Register routes
artisan_api.add_resource(ArtisanShowcaseMediaListResource, '/showcase/')
artisan_api.add_resource(ArtisanShowcaseMediaResource, '/showcase/<showcase_media_id>')
artisan_api.add_resource(ArtisanSocialListResource, '/social/')
artisan_api.add_resource(ArtisanSocialResource, '/social/<social_link_id>')
