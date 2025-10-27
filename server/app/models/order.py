from datetime import datetime
import enum
import uuid
from . import db

class OrderStatus(enum.Enum):
    cart = "cart"
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    completed = "completed"
    cancelled = "cancelled"
    refunded = "refunded"

class Order(db.Model):
    __tablename__ = "orders"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    status = db.Column(db.Enum(OrderStatus))
    total_amount = db.Column(db.Numeric(12, 2))
    currency = db.Column(db.String(3))
    shipping_address = db.Column(db.Text)
    billing_address = db.Column(db.Text)
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta_data = db.Column(db.Text)

class OrderItem(db.Model):
    __tablename__ = "order_items"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric(12, 2))
    total_price = db.Column(db.Numeric(12, 2))