from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum
import uuid

db = SQLAlchemy()

class UserRole(enum.Enum):
    buyer = "buyer"
    artisan = "artisan"
    admin = "admin"

class OrderStatus(enum.Enum):
    cart = "cart"
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    completed = "completed"
    cancelled = "cancelled"
    refunded = "refunded"

class PaymentMethod(enum.Enum):
    mpesa = "mpesa"

class PaymentStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    refunded = "refunded"

class NotificationType(enum.Enum):
    message = "message"
    order_update = "order_update"
    payment = "payment"
    system = "system"

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

class Category(db.Model):
    __tablename__ = "categories"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Subcategory(db.Model):
    __tablename__ = "subcategories"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Collection(db.Model):
    __tablename__ = "collections"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    media = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(db.Model):
    __tablename__ = "products"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    collection_id = db.Column(db.String(36), db.ForeignKey('collections.id'))
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'))
    subcategory_id = db.Column(db.String(36), db.ForeignKey('subcategories.id'))
    title = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.String(500))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3))
    stock = db.Column(db.Integer)
    meta_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

class ProductImage(db.Model):
    __tablename__ = "product_images"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    url = db.Column(db.Text, nullable=False)
    alt_text = db.Column(db.String(255))
    position = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ArtisanShowcaseMedia(db.Model):
    __tablename__ = "artisan_showcase_media"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    url = db.Column(db.Text, nullable=False)
    media_type = db.Column(db.String(20))
    caption = db.Column(db.Text)
    position = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ArtisanSocial(db.Model):
    __tablename__ = "artisan_socials"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    platform = db.Column(db.String(50))
    handle = db.Column(db.String(255))
    url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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

class Favorite(db.Model):
    __tablename__ = "favorites"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Follow(db.Model):
    __tablename__ = "follows"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    follower_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ArtisanAnalytics(db.Model):
    __tablename__ = "artisan_analytics"
    
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'), primary_key=True)
    total_sales_amount = db.Column(db.Numeric(14, 2))
    total_orders = db.Column(db.BigInteger)
    total_items_sold = db.Column(db.BigInteger)
    last_30_days_sales = db.Column(db.Numeric(14, 2))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Conversation(db.Model):
    __tablename__ = "conversations"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ConversationParticipant(db.Model):
    __tablename__ = "conversation_participants"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    __tablename__ = "messages"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id'))
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    receiver_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    message_text = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.Text)
    status = db.Column(db.String(20), default='sent')
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = "notifications"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    type = db.Column(db.Enum(NotificationType), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    related_id = db.Column(db.String(36))
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
