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
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=10)
    currency = db.Column(db.String(10), default='KSH')
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=True)
    subcategory_id = db.Column(db.String(36), db.ForeignKey('subcategories.id'), nullable=True)
    image_url = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    category = db.relationship('Category', backref='products', lazy='joined')
    subcategory = db.relationship('Subcategory', backref='products', lazy='joined')
    images = db.relationship('ProductImage', backref='product', lazy='dynamic', foreign_keys='ProductImage.product_id')

    @property
    def image(self):
        """Alias for image_url for backward compatibility"""
        return self.image_url

    @property
    def artisan_name(self):
        """Get artisan name from User model"""
        from .user import User
        artisan = User.query.get(self.artisan_id)
        return artisan.full_name if artisan else 'Unknown Artisan'

class ProductImage(db.Model):
    __tablename__ = "product_images"
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    url = db.Column(db.Text, nullable=False)
    alt_text = db.Column(db.String(255))
    position = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)