from flask_restful import Resource, Api
from flask import Blueprint, request
from models import db, Order

order_bp = Blueprint('order_bp', __name__)
order_api = Api(order_bp)

class OrderListResource(Resource):
    def post(self):
        data = request.json
        order = Order(**data)
        db.session.add(order)
        db.session.commit()
        return {'id': order.id}, 201

class OrderResource(Resource):
    def get(self, order_id):
        order = Order.query.get_or_404(order_id)
        return {
            'id': order.id,
            'status': order.status.value,
            'total_amount': float(order.total_amount),
            'placed_at': order.placed_at.isoformat()
        }

order_api.add_resource(OrderListResource, '/')
order_api.add_resource(OrderResource, '/<order_id>')