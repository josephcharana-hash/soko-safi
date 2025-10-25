from flask_socketio import SocketIO
from flask_session import Session
from app.models import db

socketio = SocketIO(cors_allowed_origins="*")
session = Session()

# Connected users storage
connected_users = {}