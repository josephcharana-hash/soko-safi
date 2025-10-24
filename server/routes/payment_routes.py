from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Payment

payment_bp = Blueprint('payment_bp', __name__)
payment_api = Api(payment_bp)

class PaymentListResource(Resource):
    def post(self):
        data = request.json
        payment = Payment(**data)
        db.session.add(payment)
        db.session.commit()
        return {'id': payment.id}, 201

class PaymentResource(Resource):
    def get(self, payment_id):
        payment = Payment.query.get_or_404(payment_id)
        return {
            'id': payment.id,
            'status': payment.status.value,
            'amount': float(payment.amount),
            'mpesa_transaction_id': payment.mpesa_transaction_id
        }

payment_api.add_resource(PaymentListResource, '/')
payment_api.add_resource(PaymentResource, '/<payment_id>')