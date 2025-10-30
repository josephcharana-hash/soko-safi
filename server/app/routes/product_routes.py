from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Product, Category, Subcategory
from app.auth import require_auth, require_role, require_ownership_or_role

product_bp = Blueprint('product_bp', __name__)
product_api = Api(product_bp)

class ProductListResource(Resource):
    def get(self):
        """Get all products - Public access"""
        try:
            products = Product.query.filter_by(deleted_at=None).all()
            return [{
                'id': p.id,
                'artisan_id': p.artisan_id,
                'artisan_name': p.artisan_name,
                'title': p.title,
                'price': float(p.price) if p.price else 0,
                'description': p.description,
                'stock': p.stock,
                'currency': p.currency or 'KSH',
                'image': p.image,
                'status': p.status or 'active',
                'category': p.category.name if p.category else None,
                'subcategory': p.subcategory.name if p.subcategory else None,
                'created_at': p.created_at.isoformat() if p.created_at else None
            } for p in products]
        except Exception as e:
            return {'error': 'Failed to fetch products'}, 500
    
    @require_role('artisan', 'admin')
    def post(self):
        """Create new product - Artisan or Admin only"""
        try:
            from flask import session
            from app.models import Category, Subcategory
            
            data = request.json or {}
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            # Required fields validation
            required_fields = ['title', 'description', 'price']
            for field in required_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400
            
            # Set artisan_id to current user if not admin
            artisan_id = session.get('user_id')
            if session.get('user_role') == 'admin' and 'artisan_id' in data:
                artisan_id = data['artisan_id']
            
            # Get image URL from frontend (already uploaded to Cloudinary)
            image_url = data.get('image')
            
            # Get or create category and subcategory
            category_id = None
            subcategory_id = None
            
            if data.get('category'):
                category = Category.query.filter_by(name=data['category']).first()
                if not category:
                    category = Category(name=data['category'])
                    db.session.add(category)
                    db.session.flush()  # Get the ID
                category_id = category.id
            
            if data.get('subcategory') and category_id:
                subcategory = Subcategory.query.filter_by(name=data['subcategory'], category_id=category_id).first()
                if not subcategory:
                    subcategory = Subcategory(name=data['subcategory'], category_id=category_id)
                    db.session.add(subcategory)
                    db.session.flush()  # Get the ID
                subcategory_id = subcategory.id
            
            # Create product
            product = Product(
                artisan_id=artisan_id,
                title=data['title'],
                description=data['description'],
                price=float(data['price']),
                stock=int(data.get('stock', 1)),
                currency=data.get('currency', 'KSH'),
                category_id=category_id,
                subcategory_id=subcategory_id,
                status='active'
            )
            
            db.session.add(product)
            db.session.flush()  # Get product ID
            
            # Add image if provided
            if image_url:
                from app.models.product import ProductImage
                product_image = ProductImage(
                    product_id=product.id,
                    url=image_url,
                    position=1
                )
                db.session.add(product_image)
            
            db.session.commit()
            
            return {
                'message': 'Product created successfully',
                'product': {
                    'id': product.id,
                    'title': product.title,
                    'price': float(product.price),
                    'image': product.image,
                    'status': product.status
                }
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create product: {str(e)}'}, 500

class ProductResource(Resource):
    def get(self, product_id):
        """Get product details - Public access"""
        try:
            product = Product.query.get_or_404(product_id)
            return {
                'id': product.id,
                'artisan_id': product.artisan_id,
                'artisan_name': product.artisan_name,
                'title': product.title,
                'price': float(product.price) if product.price else 0,
                'description': product.description,
                'stock': product.stock,
                'currency': product.currency or 'KSH',
                'image': product.image,
                'status': product.status or 'active',
                'category': product.category.name if product.category else None,
                'subcategory': product.subcategory.name if product.subcategory else None,
                'created_at': product.created_at.isoformat() if product.created_at else None
            }
        except Exception as e:
            return {'error': 'Product not found'}, 404
    
    @require_ownership_or_role('artisan_id', 'admin')
    def put(self, product_id):
        """Update product - Owner (artisan) or Admin only"""
        try:
            product = Product.query.get_or_404(product_id)
            data = request.json
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            # Update allowed fields
            if 'title' in data:
                product.title = data['title']
            if 'description' in data:
                product.description = data['description']
            if 'price' in data:
                if data['price'] < 0:
                    return {'error': 'Price cannot be negative'}, 400
                product.price = data['price']
            if 'stock' in data:
                if data['stock'] < 0:
                    return {'error': 'Stock cannot be negative'}, 400
                product.stock = data['stock']
            if 'currency' in data:
                product.currency = data['currency']
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to update product'}, 500
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
        try:
            product = Product.query.get_or_404(product_id)
            from datetime import datetime
            product.deleted_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to delete product'}, 500
        return {'message': 'Product deleted successfully'}, 200

product_api.add_resource(ProductListResource, '/')
product_api.add_resource(ProductResource, '/<product_id>')