from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Collection, Product
from app.auth import require_auth, require_role

collection_bp = Blueprint('collection_bp', __name__)
collection_api = Api(collection_bp)

class CollectionListResource(Resource):
    def get(self):
        collections = Collection.query.all()
        return [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'artisan_id': c.artisan_id,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in collections]
    
    @require_role('artisan', 'admin')
    def post(self):
        try:
            from flask import session
            data = request.json
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            if session.get('user_role') != 'admin':
                data['artisan_id'] = session.get('user_id')
            
            collection = Collection(**data)
            db.session.add(collection)
            db.session.commit()
            return {'id': collection.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create collection'}, 500

class CollectionResource(Resource):
    def get(self, collection_id):
        collection = Collection.query.get_or_404(collection_id)
        products = Product.query.filter_by(collection_id=collection_id, deleted_at=None).all()
        
        return {
            'id': collection.id,
            'title': collection.title,
            'description': collection.description,
            'artisan_id': collection.artisan_id,
            'created_at': collection.created_at.isoformat() if collection.created_at else None,
            'products': [{
                'id': p.id,
                'title': p.title,
                'price': float(p.price) if p.price else 0,
                'description': p.description
            } for p in products]
        }

collection_api.add_resource(CollectionListResource, '/')
collection_api.add_resource(CollectionResource, '/<collection_id>')