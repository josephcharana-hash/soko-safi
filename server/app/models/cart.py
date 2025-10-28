from datetime import datetime
import uuid
from . import db

class Cart(db.Model):
    __tablename__ = "carts"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta_data = db.Column(db.Text)

class CartItem(db.Model):
    __tablename__ = "cart_items"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cart_id = db.Column(db.String(36), db.ForeignKey('carts.id'))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric(12, 2))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)