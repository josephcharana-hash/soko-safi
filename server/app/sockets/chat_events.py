from flask import request
from flask_socketio import emit, join_room
from app.extensions import socketio, connected_users, db
from app.models.message import Message

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
    user_id = data['user_id']
    connected_users[user_id] = request.sid
    join_room(f'user_{user_id}')
    emit('status', {'msg': f'User {user_id} joined'})

@socketio.on('send_message')
def handle_message(data):
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message_text = data['message']
    
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
        socketio.emit('new_message', {
            'id': message.id,
            'sender_id': sender_id,
            'message': message_text,
            'timestamp': message.timestamp.isoformat()
        }, room=connected_users[receiver_id])
    
    # Confirm to sender
    emit('message_sent', {'status': 'delivered', 'message_id': message.id})

@socketio.on('get_chat_history')
def handle_chat_history(data):
    user1 = data['user1']
    user2 = data['user2']
    
    messages = Message.query.filter(
        ((Message.sender_id == user1) & (Message.receiver_id == user2)) |
        ((Message.sender_id == user2) & (Message.receiver_id == user1))
    ).order_by(Message.timestamp).all()
    
    chat_history = [{
        'id': msg.id,
        'sender_id': msg.sender_id,
        'receiver_id': msg.receiver_id,
        'message': msg.message,
        'timestamp': msg.timestamp.isoformat(),
        'is_read': msg.is_read
    } for msg in messages]
    
    emit('chat_history', {'messages': chat_history})