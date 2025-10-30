from flask_socketio import SocketIO
from flask_session import Session
from flask_cors import CORS
from app.models import db
import os

try:
    # Initialize extensions with proper error handling
    allowed_origins = os.getenv('CORS_ALLOWED_ORIGINS', '*').split(',')
    socketio = SocketIO(cors_allowed_origins=allowed_origins)
    session = Session()
    cors = CORS()
    
    # Connected users storage
    connected_users = {}
except Exception as e:
    print(f"Failed to initialize extensions: {e}")
    raise