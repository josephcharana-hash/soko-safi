from datetime import datetime
import uuid
from . import db
from enum import Enum

class MessageType(Enum):
    TEXT = 'text'
    IMAGE = 'image'
    FILE = 'file'

class MessageStatus(Enum):
    SENT = 'sent'
    DELIVERED = 'delivered'
    READ = 'read'

class Message(db.Model):
    __tablename__ = "messages"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    message_type = db.Column(db.Enum(MessageType), default=MessageType.TEXT)
    attachment_url = db.Column(db.String(500), nullable=True)
    attachment_name = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(MessageStatus), default=MessageStatus.SENT)
    deleted_at = db.Column(db.DateTime, nullable=True)