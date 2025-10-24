from datetime import datetime
import enum
import uuid
from . import db

class PaymentMethod(enum.Enum):
    mpesa = "mpesa"

class PaymentStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    refunded = "refunded"

class Payment(db.Model):
    __tablename__ = "payments"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'))
    amount = db.Column(db.Numeric(12, 2))
    currency = db.Column(db.String(3))
    status = db.Column(db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    mpesa_transaction_id = db.Column(db.String(255), unique=True)
    payer_phone = db.Column(db.String(30))
    callback_payload = db.Column(db.Text)
    transaction_status_reason = db.Column(db.Text)
    reversal_flag = db.Column(db.Boolean, default=False)
    reversal_timestamp = db.Column(db.DateTime)
    received_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)