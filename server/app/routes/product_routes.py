from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Product
from app.auth import require_auth, require_role, require_ownership_or_role

product_bp = Blueprint('product_bp', __name__)
product_api = Api(product_bp)

class ProductListResource(Resource):
    def get(self):
        """Get all products - Public access"""
        products = Product.query.filter_by(deleted_at=None).all()
        return [{
            'id': p.id,
            'artisan_id': p.artisan_id,
            'title': p.title,
            'price': float(p.price),
            'description': p.description,
            'stock': p.stock,
            'currency': p.currency,
            'created_at': p.created_at.isoformat() if p.created_at else None
        } for p in products]
    
    @require_role('artisan', 'admin')
    def post(self):
        """Create new product - Artisan or Admin only"""
        try:
            data = request.json
            if not data:
                return {'error': 'No data provided'}, 400
            
            from flask import session
            
            # Set artisan_id to current user if not admin
            if session.get('user_role') != 'admin':
                data['artisan_id'] = session.get('user_id')
            
            product = Product(**data)
            db.session.add(product)
            db.session.commit()
            return {'id': product.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create product'}, 500

class ProductResource(Resource):
    def get(self, product_id):
        """Get product details - Public access"""
        product = Product.query.get_or_404(product_id)
        return {
            'id': product.id,
            'artisan_id': product.artisan_id,
            'title': product.title,
            'price': float(product.price),
            'description': product.description,
            'stock': product.stock,
            'currency': product.currency,
            'created_at': product.created_at.isoformat() if product.created_at else None
        }
    
    @require_ownership_or_role('artisan_id', 'admin')
    def put(self, product_id):
        """Update product - Owner (artisan) or Admin only"""
        product = Product.query.get_or_404(product_id)
        data = request.json
        
        # Update allowed fields
        if 'title' in data:
            product.title = data['title']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'stock' in data:
            product.stock = data['stock']
        if 'currency' in data:
            product.currency = data['currency']
        
        db.session.commit()
        return {
            'message': 'Product updated successfully',
            'product': {
                'id': product.id,
                'artisan_id': product.artisan_id,
                'title': product.title,
                'price': float(product.price),
                'description': product.description,
                'stock': product.stock,
                'currency': product.currency
            }
        }, 200
    
    @require_ownership_or_role('artisan_id', 'admin')
    def delete(self, product_id):
        """Delete product - Owner (artisan) or Admin only"""
        product = Product.query.get_or_404(product_id)
        from datetime import datetime
        product.deleted_at = datetime.utcnow()
        db.session.commit()
        return {'message': 'Product deleted successfully'}, 200

product_api.add_resource(ProductListResource, '/')
product_api.add_resource(ProductResource, '/<product_id>')