from flask_socketio import SocketIO
from app.models import db

socketio = SocketIO(cors_allowed_origins="*")

# Connected users storage
connected_users = {}