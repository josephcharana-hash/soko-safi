#!/usr/bin/env python3
import socketio
import time

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to WebSocket server")

@sio.event
def disconnect():
    print("❌ Disconnected from server")

@sio.event
def status(data):
    print(f"📢 Status: {data['msg']}")

@sio.event
def new_message(data):
    print(f"💬 New message from {data['sender_id']}: {data['message']}")

@sio.event
def message_sent(data):
    print(f"✅ Message sent: {data['status']}")

@sio.event
def notification(data):
    print(f"🔔 Notification [{data['type']}]: {data['data']['message']}")

@sio.event
def chat_history(data):
    print("📜 Chat History:")
    for msg in data['messages']:
        print(f"  {msg['sender_id']} → {msg['receiver_id']}: {msg['message']}")

def test_websocket():
    try:
        # Connect to server
        print("🔌 Connecting to WebSocket server...")
        sio.connect('http://localhost:5000')
        
        # Join as user 1
        print("👤 Joining as User 1...")
        sio.emit('join', {'user_id': 1})
        time.sleep(1)
        
        # Send a message
        print("📤 Sending message to User 2...")
        sio.emit('send_message', {
            'sender_id': 1,
            'receiver_id': 2,
            'message': 'Hello from terminal test!'
        })
        time.sleep(1)
        
        # Get chat history
        print("📋 Getting chat history...")
        sio.emit('get_chat_history', {'user1': 1, 'user2': 2})
        time.sleep(2)
        
        print("✅ WebSocket test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        sio.disconnect()

if __name__ == '__main__':
    test_websocket()