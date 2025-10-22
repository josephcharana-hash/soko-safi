from flask import Blueprint, request, jsonify
from models import db, Order

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    order = Order(**data)
    db.session.add(order)
    db.session.commit()
    return jsonify({'id': order.id}), 201

@order_bp.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'status': order.status.value,
        'total_amount': float(order.total_amount),
        'placed_at': order.placed_at.isoformat()
    })