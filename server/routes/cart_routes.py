from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Cart, CartItem

cart_bp = Blueprint('cart_bp', __name__)
cart_api = Api(cart_bp)

class CartResource(Resource):
    def get(self, user_id):
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            return {'items': []}
        
        items = CartItem.query.filter_by(cart_id=cart.id).all()
        return {
            'items': [{
                'id': item.id,
                'product_id': item.product_id,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price)
            } for item in items]
        }

class CartItemResource(Resource):
    def post(self):
        data = request.json
        cart_item = CartItem(**data)
        db.session.add(cart_item)
        db.session.commit()
        return {'id': cart_item.id}, 201

cart_api.add_resource(CartResource, '/<user_id>')
cart_api.add_resource(CartItemResource, '/items')