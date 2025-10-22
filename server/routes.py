from flask import Blueprint, request, jsonify
from models import *

api = Blueprint('api', __name__)

# Users
@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201

@api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'role': user.role.value,
        'email': user.email,
        'full_name': user.full_name,
        'phone': user.phone,
        'location': user.location
    })

# Products
@api.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id}), 201

@api.route('/products', methods=['GET'])
def get_products():
    products = Product.query.filter_by(deleted_at=None).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'price': float(p.price),
        'description': p.description,
        'stock': p.stock
    } for p in products])

@api.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'title': product.title,
        'price': float(product.price),
        'description': product.description,
        'stock': product.stock
    })

# Orders
@api.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = Order(**data)
    db.session.add(order)
    db.session.commit()
    return jsonify({'id': order.id}), 201

@api.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'status': order.status.value,
        'total_amount': float(order.total_amount),
        'placed_at': order.placed_at.isoformat()
    })

# Cart
@api.route('/cart/<user_id>', methods=['GET'])
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

@api.route('/cart/items', methods=['POST'])
def add_to_cart():
    data = request.json
    cart_item = CartItem(**data)
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({'id': cart_item.id}), 201

# Categories
@api.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in categories])

@api.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    category = Category(**data)
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id}), 201

# Reviews
@api.route('/products/<product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([{
        'id': r.id,
        'rating': r.rating,
        'title': r.title,
        'body': r.body,
        'created_at': r.created_at.isoformat()
    } for r in reviews])

@api.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    review = Review(**data)
    db.session.add(review)
    db.session.commit()
    return jsonify({'id': review.id}), 201

# Messages
@api.route('/conversations/<conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    messages = Message.query.filter_by(conversation_id=conversation_id).all()
    return jsonify([{
        'id': m.id,
        'sender_id': m.sender_id,
        'message_text': m.message_text,
        'created_at': m.created_at.isoformat()
    } for m in messages])

@api.route('/messages', methods=['POST'])
def send_message():
    data = request.json
    message = Message(**data)
    db.session.add(message)
    db.session.commit()
    return jsonify({'id': message.id}), 201

# Payments
@api.route('/payments', methods=['POST'])
def create_payment():
    data = request.json
    payment = Payment(**data)
    db.session.add(payment)
    db.session.commit()
    return jsonify({'id': payment.id}), 201

@api.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify({
        'id': payment.id,
        'status': payment.status.value,
        'amount': float(payment.amount),
        'mpesa_transaction_id': payment.mpesa_transaction_id
    })