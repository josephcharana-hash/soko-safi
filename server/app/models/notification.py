from datetime import datetime
import enum
import uuid
from . import db

class NotificationType(enum.Enum):
    message = "message"
    order_update = "order_update"
    payment = "payment"
    system = "system"

class Notification(db.Model):
    __tablename__ = "notifications"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    type = db.Column(db.Enum(NotificationType))
    title = db.Column(db.String(255))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)