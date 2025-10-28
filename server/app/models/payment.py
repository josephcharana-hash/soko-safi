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

class DisbursementStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"
    retry = "retry"
    manual = "manual"  # Requires admin intervention

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

class ArtisanDisbursement(db.Model):
    __tablename__ = "artisan_disbursements"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    payment_id = db.Column(db.String(36), db.ForeignKey('payments.id'))
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    amount = db.Column(db.Numeric(12, 2))
    currency = db.Column(db.String(3), default='KES')
    status = db.Column(db.Enum(DisbursementStatus), nullable=False, default=DisbursementStatus.pending)
    mpesa_transaction_id = db.Column(db.String(255), unique=True)
    recipient_phone = db.Column(db.String(15))  # For phone disbursements
    paybill_number = db.Column(db.String(10))  # For paybill disbursements
    paybill_account = db.Column(db.String(50))  # Account reference
    disbursement_method = db.Column(db.String(20))  # 'phone' or 'paybill'
    retry_count = db.Column(db.Integer, default=0)
    last_retry_at = db.Column(db.DateTime)
    failure_reason = db.Column(db.Text)
    callback_payload = db.Column(db.Text)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)