from datetime import datetime
import uuid
from . import db

class Review(db.Model):
    __tablename__ = "reviews"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    rating = db.Column(db.SmallInteger)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)