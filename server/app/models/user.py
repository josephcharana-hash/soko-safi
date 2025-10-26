from datetime import datetime
import enum
import uuid
from . import db

class UserRole(enum.Enum):
    buyer = "buyer"
    artisan = "artisan"
    admin = "admin"

class PaymentMethod(enum.Enum):
    phone = "phone"
    paybill = "paybill"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    role = db.Column(db.Enum(UserRole), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    phone = db.Column(db.String(30))
    description = db.Column(db.Text)
    profile_picture_url = db.Column(db.Text)
    banner_image_url = db.Column(db.Text)
    location = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean)
    meta_data = db.Column(db.Text)

    # Artisan payment method fields
    payment_method = db.Column(db.Enum(PaymentMethod))  # phone or paybill
    mpesa_phone = db.Column(db.String(15))  # +254XXXXXXXXX format
    paybill_number = db.Column(db.String(10))  # Paybill number
    paybill_account = db.Column(db.String(50))  # Account reference for paybill

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)