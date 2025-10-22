from flask import Blueprint, request, jsonify
from models import db, Cart, CartItem

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/<user_id>', methods=['GET'])
def get_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'items': []})
    
    items = CartItem.query.filter_by(cart_id=cart.id).all()
    return jsonify({
        'items': [{
            'id': item.id,
            'product_id': item.product_id,
            'quantity': item.quantity,
            'unit_price': float(item.unit_price)
        } for item in items]
    })

@cart_bp.route('/items', methods=['POST'])
def add_to_cart():
    data = request.json
    cart_item = CartItem(**data)
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({'id': cart_item.id}), 201