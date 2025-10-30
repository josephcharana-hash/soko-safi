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
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add properties for compatibility
    @property
    def title(self):
        return self.name
    
    @property
    def artisan_id(self):
        return None
    
    @property
    def currency(self):
        return 'KSH'
    
    @property
    def stock(self):
        return 10
    
    @property
    def status(self):
        return 'active'
    
    @property
    def category(self):
        return None
    
    @property
    def subcategory(self):
        return None
    
    @property
    def deleted_at(self):
        return None
    
    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy='dynamic', foreign_keys='ProductImage.product_id')
    
    @property
    def image_url(self):
        """Get main image URL from first ProductImage"""
        first_image = self.images.first()
        return first_image.url if first_image else None
    
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
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    url = db.Column(db.Text, nullable=False)
    alt_text = db.Column(db.String(255))
    position = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)