from flask import request
from flask_socketio import emit, join_room
from app.extensions import socketio, connected_users
from app.models import db, Message

@socketio.on('connect')
def handle_connect():
    print(f'Client {request.sid} connected')
    emit('status', {'msg': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    user_id = None
    for uid, sid in connected_users.items():
        if sid == request.sid:
            user_id = uid
            break
    if user_id:
        del connected_users[user_id]
    print(f'Client {request.sid} disconnected')

@socketio.on('join')
def handle_join(data):
    try:
        if not data or 'user_id' not in data:
            emit('error', {'msg': 'user_id is required'})
            return
        
        user_id = data['user_id']
        connected_users[user_id] = request.sid
        join_room(f'user_{user_id}')
        emit('status', {'msg': f'User {user_id} joined'})
    except Exception as e:
        print(f'Error in handle_join: {e}')
        emit('error', {'msg': 'Failed to join'})

@socketio.on('send_message')
def handle_message(data):
    try:
        if not data or not all(k in data for k in ['sender_id', 'receiver_id', 'message']):
            emit('error', {'msg': 'sender_id, receiver_id, and message are required'})
            return
        
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        message_text = data['message']
        
        if not message_text or len(message_text.strip()) == 0:
            emit('error', {'msg': 'Message cannot be empty'})
            return
        
        # Save to database
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message_text
        )
        db.session.add(message)
        db.session.commit()
        
        # Send to receiver if online
        if receiver_id in connected_users:
            # Sanitize message content to prevent XSS
            import html
            safe_message = html.escape(str(message_text))
            socketio.emit('new_message', {
                'id': message.id,
                'sender_id': sender_id,
                'message': safe_message,
                'timestamp': message.timestamp.isoformat()
            }, room=connected_users[receiver_id])
        
        # Confirm to sender
        emit('message_sent', {'status': 'delivered', 'message_id': message.id})
    except Exception as e:
        db.session.rollback()
        print(f'Error in handle_message: {e}')
        emit('error', {'msg': 'Failed to send message'})

@socketio.on('get_chat_history')
def handle_chat_history(data):
    try:
        if not data or not all(k in data for k in ['user1', 'user2']):
            emit('error', {'msg': 'user1 and user2 are required'})
            return
        
        user1 = data['user1']
        user2 = data['user2']
        
        messages = Message.query.filter(
            ((Message.sender_id == user1) & (Message.receiver_id == user2)) |
            ((Message.sender_id == user2) & (Message.receiver_id == user1))
        ).order_by(Message.timestamp).limit(100).all()  # Limit to prevent large responses
        
        chat_history = [{
            'id': msg.id,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'message': msg.message,
            'timestamp': msg.timestamp.isoformat() if msg.timestamp else None,
            'is_read': msg.is_read
        } for msg in messages]
        
        emit('chat_history', {'messages': chat_history})
    except Exception as e:
        print(f'Error in handle_chat_history: {e}')
        emit('error', {'msg': 'Failed to get chat history'})