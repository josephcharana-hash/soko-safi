"""
Notification routes for Soko Safi
Handles CRUD operations for notifications
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Notification, NotificationType
from app.auth import require_auth, require_role, require_ownership_or_role

notification_bp = Blueprint('notification_bp', __name__)
notification_api = Api(notification_bp)

class NotificationListResource(Resource):
    @require_auth
    def get(self):
        """Get all notifications - Admin only"""
        from flask import session
        if session.get('user_role') != 'admin':
            return {'error': 'Admin access required'}, 403
        
        notifications = Notification.query.filter_by(deleted_at=None).all()
        return [{
            'id': n.id,
            'user_id': n.user_id,
            'type': n.type.value if n.type else None,
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat() if n.created_at else None
        } for n in notifications]
    
    @require_auth
    def post(self):
        """Create new notification - Authenticated users only"""
        from flask import session
        data = request.json
        
        # Set user_id to current user if not admin
        if session.get('user_role') != 'admin':
            data['user_id'] = session.get('user_id')
        
        notification = Notification(**data)
        db.session.add(notification)
        db.session.commit()
        
        return {
            'message': 'Notification created successfully',
            'notification': {
                'id': notification.id,
                'user_id': notification.user_id,
                'type': notification.type.value if notification.type else None,
                'title': notification.title,
                'message': notification.message
            }
        }, 201

class NotificationResource(Resource):
    @require_ownership_or_role('user_id', 'admin')
    def get(self, notification_id):
        """Get notification details - Owner or Admin only"""
        notification = Notification.query.get_or_404(notification_id)
        return {
            'id': notification.id,
            'user_id': notification.user_id,
            'type': notification.type.value if notification.type else None,
            'title': notification.title,
            'message': notification.message,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat() if notification.created_at else None
        }
    
    @require_ownership_or_role('user_id', 'admin')
    def put(self, notification_id):
        """Update notification - Owner or Admin only"""
        notification = Notification.query.get_or_404(notification_id)
        data = request.json
        
        if 'type' in data:
            notification.type = NotificationType(data['type'])
        if 'title' in data:
            notification.title = data['title']
        if 'message' in data:
            notification.message = data['message']
        if 'is_read' in data:
            notification.is_read = data['is_read']
        if 'user_id' in data and session.get('user_role') == 'admin':
            notification.user_id = data['user_id']
        
        db.session.commit()
        
        return {
            'message': 'Notification updated successfully',
            'notification': {
                'id': notification.id,
                'user_id': notification.user_id,
                'type': notification.type.value if notification.type else None,
                'title': notification.title,
                'message': notification.message,
                'is_read': notification.is_read
            }
        }, 200
    
    @require_ownership_or_role('user_id', 'admin')
    def delete(self, notification_id):
        """Delete notification - Owner or Admin only"""
        notification = Notification.query.get_or_404(notification_id)
        from datetime import datetime
        notification.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'message': 'Notification deleted successfully'}, 200

# Register routes
notification_api.add_resource(NotificationListResource, '/')
notification_api.add_resource(NotificationResource, '/<notification_id>')
