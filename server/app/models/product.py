from datetime import datetime
import uuid
from . import db

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