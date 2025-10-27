from datetime import datetime
import uuid
from . import db

class Favorite(db.Model):
    __tablename__ = "favorites"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)