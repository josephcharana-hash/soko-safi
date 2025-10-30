from flask_restful import Resource, Api
from flask import Blueprint, request, session
from app.models.product import Product
from app.models import db

product_bp = Blueprint('product_bp', __name__)
product_api = Api(product_bp)

class ProductListResource(Resource):
    def get(self):
        try:
            products = Product.query.filter_by(status='active').all()
            print(f"Found {len(products)} products in database")
            return [{
                'id': p.id,
                'title': p.title,
                'price': p.price,
                'description': p.description,
                'image_url': p.image_url,
                'stock': p.stock,
                'currency': p.currency,
                'status': p.status
            } for p in products]
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []
    
    def post(self):
        try:
            if request.is_json:
                data = request.json or {}
            else:
                data = request.form.to_dict()

            if not data:
                return {'error': 'No data provided'}, 400

            required_fields = ['title', 'description', 'price']
            for field in required_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400

            product = Product(
                title=data['title'],
                description=data['description'],
                price=float(data['price']),
                image_url=data.get('image', data.get('image_url', '')),
                artisan_id=session.get('user_id'),
                stock=int(data.get('stock', 10)),
                currency=data.get('currency', 'KSH')
            )
            
            db.session.add(product)
            db.session.commit()

            return {
                'message': 'Product created successfully',
                'product': {
                    'id': product.id,
                    'title': product.title,
                    'price': product.price,
                    'image_url': product.image_url,
                    'status': product.status
                }
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create product: {str(e)}'}, 500

class ProductResource(Resource):
    def get(self, product_id):
        try:
            product = Product.query.get(product_id)
            if not product:
                return {'error': 'Product not found'}, 404
            
            return {
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'description': product.description,
                'stock': product.stock,
                'currency': product.currency,
                'image_url': product.image_url,
                'status': product.status
            }
        except Exception:
            return {'error': 'Product not found'}, 404
    
    def put(self, product_id):
        try:
            product = Product.query.get(product_id)
            if not product:
                return {'error': 'Product not found'}, 404
            
            data = request.json or {}
            if 'title' in data:
                product.title = data['title']
            if 'price' in data:
                product.price = float(data['price'])
            if 'description' in data:
                product.description = data['description']
            if 'stock' in data:
                product.stock = int(data['stock'])
            if 'image_url' in data:
                product.image_url = data['image_url']
            
            db.session.commit()
            return {'message': 'Product updated successfully'}, 200
        except Exception:
            db.session.rollback()
            return {'error': 'Failed to update product'}, 500
    
    def delete(self, product_id):
        try:
            product = Product.query.get(product_id)
            if not product:
                return {'error': 'Product not found'}, 404
            
            product.status = 'deleted'
            db.session.commit()
            return {'message': 'Product deleted successfully'}, 200
        except Exception:
            db.session.rollback()
            return {'error': 'Failed to delete product'}, 500

product_api.add_resource(ProductListResource, '/')
product_api.add_resource(ProductResource, '/<product_id>')