from flask import Blueprint, request, jsonify
from models import db, Payment

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/', methods=['POST'])
def create_payment():
    data = request.json
    payment = Payment(**data)
    db.session.add(payment)
    db.session.commit()
    return jsonify({'id': payment.id}), 201

@payment_bp.route('/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify({
        'id': payment.id,
        'status': payment.status.value,
        'amount': float(payment.amount),
        'mpesa_transaction_id': payment.mpesa_transaction_id
    })