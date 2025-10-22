from flask import Blueprint, request, jsonify
from models import db, Product

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.json
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id}), 201

@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.filter_by(deleted_at=None).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'price': float(p.price),
        'description': p.description,
        'stock': p.stock
    } for p in products])

@product_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'title': product.title,
        'price': float(product.price),
        'description': product.description,
        'stock': product.stock
    })