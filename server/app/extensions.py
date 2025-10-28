from flask_socketio import SocketIO
from flask_session import Session
from flask_cors import CORS
from app.models import db

socketio = SocketIO(cors_allowed_origins="*")
session = Session()
cors = CORS()

# Connected users storage
connected_users = {}