from flask import Blueprint, request, jsonify
from models import db, Message

message_bp = Blueprint('message_bp', __name__)

@message_bp.route('/conversations/<conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    messages = Message.query.filter_by(conversation_id=conversation_id).all()
    return jsonify([{
        'id': m.id,
        'sender_id': m.sender_id,
        'message_text': m.message_text,
        'created_at': m.created_at.isoformat()
    } for m in messages])

@message_bp.route('/', methods=['POST'])
def send_message():
    data = request.json
    message = Message(**data)
    db.session.add(message)
    db.session.commit()
    return jsonify({'id': message.id}), 201