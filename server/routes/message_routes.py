from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Message

message_bp = Blueprint('message_bp', __name__)
message_api = Api(message_bp)

class ConversationMessageResource(Resource):
    def get(self, conversation_id):
        messages = Message.query.filter_by(conversation_id=conversation_id).all()
        return [{
            'id': m.id,
            'sender_id': m.sender_id,
            'message_text': m.message_text,
            'created_at': m.created_at.isoformat()
        } for m in messages]

class MessageListResource(Resource):
    def post(self):
        data = request.json
        message = Message(**data)
        db.session.add(message)
        db.session.commit()
        return {'id': message.id}, 201

message_api.add_resource(ConversationMessageResource, '/conversations/<conversation_id>/messages')
message_api.add_resource(MessageListResource, '/')