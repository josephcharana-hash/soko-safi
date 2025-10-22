from flask_restful import Resource, Api
from flask import Blueprint, request
from models import db, Product

product_bp = Blueprint('product_bp', __name__)
product_api = Api(product_bp)

class ProductListResource(Resource):
    def post(self):
        data = request.json
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        return {'id': product.id}, 201
    
    def get(self):
        products = Product.query.filter_by(deleted_at=None).all()
        return [{
            'id': p.id,
            'title': p.title,
            'price': float(p.price),
            'description': p.description,
            'stock': p.stock
        } for p in products]

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return {
            'id': product.id,
            'title': product.title,
            'price': float(product.price),
            'description': product.description,
            'stock': product.stock
        }

product_api.add_resource(ProductListResource, '/')
product_api.add_resource(ProductResource, '/<product_id>')