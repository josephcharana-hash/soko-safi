"""
Message routes for Soko Safi
Handles CRUD operations for messages
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Message
from app.auth import require_auth, require_role, require_ownership_or_role

message_bp = Blueprint('message_bp', __name__)
message_api = Api(message_bp)

class MessageListResource(Resource):
    @require_auth
    def get(self):
        """Get all messages - Admin only"""
        from flask import session
        if session.get('user_role') != 'admin':
            return {'error': 'Admin access required'}, 403
        
        messages = Message.query.filter_by(deleted_at=None).all()
        return [{
            'id': m.id,
            'sender_id': m.sender_id,
            'receiver_id': m.receiver_id,
            'message': m.message,
            'timestamp': m.timestamp.isoformat() if m.timestamp else None,
            'is_read': m.is_read
        } for m in messages]
    
    @require_auth
    def post(self):
        """Create new message - Authenticated users only"""
        from flask import session
        data = request.json
        
        # Set sender_id to current user if not admin
        if session.get('user_role') != 'admin':
            data['sender_id'] = session.get('user_id')
        
        message = Message(**data)
        db.session.add(message)
        db.session.commit()
        
        return {
            'message': 'Message created successfully',
            'message_data': {
                'id': message.id,
                'sender_id': message.sender_id,
                'receiver_id': message.receiver_id,
                'message': message.message
            }
        }, 201

class MessageResource(Resource):
    @require_auth
    def get(self, message_id):
        """Get message details - Sender, Receiver, or Admin only"""
        message = Message.query.get_or_404(message_id)
        
        # Check if user is sender, receiver, or admin
        from flask import session
        current_user_id = session.get('user_id')
        user_role = session.get('user_role')
        
        if user_role != 'admin' and message.sender_id != current_user_id and message.receiver_id != current_user_id:
            return {'error': 'Access denied'}, 403
        
        return {
            'id': message.id,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'message': message.message,
            'timestamp': message.timestamp.isoformat() if message.timestamp else None,
            'is_read': message.is_read
        }
    
    @require_auth
    def put(self, message_id):
        """Update message - Sender, Receiver, or Admin only"""
        message = Message.query.get_or_404(message_id)
        
        # Check if user is sender, receiver, or admin
        from flask import session
        current_user_id = session.get('user_id')
        user_role = session.get('user_role')
        
        if user_role != 'admin' and message.sender_id != current_user_id and message.receiver_id != current_user_id:
            return {'error': 'Access denied'}, 403
        
        data = request.json
        
        # Only allow updating is_read status for receiver or admin
        if 'is_read' in data and (message.receiver_id == current_user_id or user_role == 'admin'):
            message.is_read = data['is_read']
        
        # Only sender or admin can update message content
        if 'message' in data and (message.sender_id == current_user_id or user_role == 'admin'):
            message.message = data['message']
        
        if 'sender_id' in data and user_role == 'admin':
            message.sender_id = data['sender_id']
        if 'receiver_id' in data and user_role == 'admin':
            message.receiver_id = data['receiver_id']
        
        db.session.commit()
        
        return {
            'message': 'Message updated successfully',
            'message_data': {
                'id': message.id,
                'sender_id': message.sender_id,
                'receiver_id': message.receiver_id,
                'message': message.message,
                'is_read': message.is_read
            }
        }, 200
    
    @require_auth
    def delete(self, message_id):
        """Delete message - Sender, Receiver, or Admin only"""
        message = Message.query.get_or_404(message_id)
        
        # Check if user is sender, receiver, or admin
        from flask import session
        current_user_id = session.get('user_id')
        user_role = session.get('user_role')
        
        if user_role != 'admin' and message.sender_id != current_user_id and message.receiver_id != current_user_id:
            return {'error': 'Access denied'}, 403
        
        from datetime import datetime
        message.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'message': 'Message deleted successfully'}, 200

class MessageConversationsResource(Resource):
    @require_auth
    def get(self):
        """Get conversations for current user"""
        from flask import session
        from app.models import User

        current_user_id = session.get('user_id')
        user_role = session.get('user_role')

        if user_role == 'admin':
            # Admin gets all conversations (simplified for now)
            conversations = db.session.query(Message).filter(
                Message.deleted_at.is_(None)
            ).group_by(Message.sender_id, Message.receiver_id).limit(20).all()
        else:
            # Regular users get their conversations
            conversations = db.session.query(Message).filter(
                db.or_(
                    Message.sender_id == current_user_id,
                    Message.receiver_id == current_user_id
                ),
                Message.deleted_at.is_(None)
            ).order_by(Message.timestamp.desc()).limit(20).all()

        # Group by conversation partner
        conversation_partners = {}
        for msg in conversations:
            partner_id = msg.receiver_id if msg.sender_id == current_user_id else msg.sender_id
            if partner_id not in conversation_partners:
                partner = User.query.get(partner_id)
                conversation_partners[partner_id] = {
                    'partner_id': partner_id,
                    'partner_name': partner.full_name if partner else 'Unknown User',
                    'partner_email': partner.email if partner else '',
                    'last_message': msg.message,
                    'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
                    'is_read': msg.is_read,
                    'unread_count': 0
                }

        # Count unread messages for each conversation
        for partner_id, conv in conversation_partners.items():
            unread_count = Message.query.filter_by(
                sender_id=partner_id,
                receiver_id=current_user_id,
                is_read=False,
                deleted_at=None
            ).count()
            conv['unread_count'] = unread_count

        return list(conversation_partners.values())

# Register routes
message_api.add_resource(MessageListResource, '/')
message_api.add_resource(MessageResource, '/<message_id>')
message_api.add_resource(MessageConversationsResource, '/conversations')