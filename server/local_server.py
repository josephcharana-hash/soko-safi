#!/usr/bin/env python3
import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# Load local environment
from dotenv import load_dotenv
load_dotenv('.env.local')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/soko_safi.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# Enable CORS
CORS(app, origins=['http://127.0.0.1:5173', 'http://localhost:5173'], supports_credentials=True)

# Initialize extensions
db = SQLAlchemy(app)
Session(app)

# Simple models
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artisan_id = db.Column(db.String(36))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    currency = db.Column(db.String(3), default='KSH')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

class ProductImage(db.Model):
    __tablename__ = "product_images"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    url = db.Column(db.Text, nullable=False)
    alt_text = db.Column(db.String(255))
    position = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/api/categories/')
def get_categories():
    return jsonify([])

@app.route('/api/products/', methods=['GET', 'POST'])
def handle_products():
    if request.method == 'GET':
        products = Product.query.filter_by(deleted_at=None).all()
        result = []
        for p in products:
            images = ProductImage.query.filter_by(product_id=p.id).order_by(ProductImage.position).all()
            result.append({
                'id': p.id,
                'artisan_id': p.artisan_id,
                'title': p.title,
                'price': float(p.price) if p.price else 0,
                'description': p.description,
                'stock': p.stock,
                'currency': p.currency,
                'images': [{'url': img.url, 'alt_text': img.alt_text} for img in images],
                'created_at': p.created_at.isoformat() if p.created_at else None
            })
        return jsonify(result)
    
    elif request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create product
        product = Product(
            artisan_id=data.get('artisan_id', 'test-artisan'),
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            stock=data.get('stock', 10),
            currency=data.get('currency', 'KSH')
        )
        db.session.add(product)
        db.session.flush()
        
        # Add images
        images = data.get('images', [])
        for i, img_data in enumerate(images):
            image = ProductImage(
                product_id=product.id,
                url=img_data.get('url'),
                alt_text=img_data.get('alt_text', ''),
                position=i
            )
            db.session.add(image)
        
        db.session.commit()
        return jsonify({'id': product.id}), 201

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    ProductImage.query.filter_by(product_id=product_id).delete()
    product.deleted_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

@app.route('/api/auth/profile')
def get_profile():
    return jsonify({'user': {'full_name': '', 'description': '', 'location': '', 'phone': '', 'profile_picture_url': ''}})

@app.route('/api/artisan/dashboard')
def get_dashboard():
    return jsonify({'stats': {'total_products': 0, 'total_orders': 0, 'total_revenue': 0}})

@app.route('/api/cart/')
def get_cart():
    return jsonify([])

@app.route('/api/upload/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Mock response for local development
    return jsonify({
        'message': 'File uploaded successfully',
        'url': 'https://via.placeholder.com/400x400?text=Uploaded+Image',
        'public_id': 'mock_public_id'
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(host='127.0.0.1', port=5001, debug=True)