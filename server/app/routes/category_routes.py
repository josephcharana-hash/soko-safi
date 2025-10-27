"""
Category routes for Soko Safi
Handles CRUD operations for categories and subcategories
"""

from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Category, Subcategory
from app.auth import require_auth, require_role, require_ownership_or_role

category_bp = Blueprint('category_bp', __name__)
category_api = Api(category_bp)

class CategoryListResource(Resource):
    def get(self):
        """Get all categories - Public access"""
        # Support databases that don't have the soft-delete column yet
        if hasattr(Category, 'deleted_at'):
            categories = Category.query.filter_by(deleted_at=None).all()
        else:
            categories = Category.query.all()
        return [{
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in categories]
    
    @require_role('admin')
    def post(self):
        """Create new category - Admin only"""
        data = request.json
        
        if not data.get('name'):
            return {'error': 'Category name is required'}, 400
        
        category = Category(
            name=data['name'].strip(),
            description=data.get('description', '').strip()
        )
        
        db.session.add(category)
        db.session.commit()
        
        return {
            'message': 'Category created successfully',
            'category': {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
        }, 201

class CategoryResource(Resource):
    def get(self, category_id):
        """Get category details - Public access"""
        category = Category.query.get_or_404(category_id)
        return {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'created_at': category.created_at.isoformat() if category.created_at else None
        }
    
    @require_role('admin')
    def put(self, category_id):
        """Update category - Admin only"""
        category = Category.query.get_or_404(category_id)
        data = request.json
        
        if 'name' in data:
            category.name = data['name'].strip()
        if 'description' in data:
            category.description = data['description'].strip()
        
        db.session.commit()
        
        return {
            'message': 'Category updated successfully',
            'category': {
                'id': category.id,
            'name': category.name,
                'description': category.description
            }
        }, 200
    
    @require_role('admin')
    def delete(self, category_id):
        """Delete category - Admin only"""
        category = Category.query.get_or_404(category_id)
        from datetime import datetime
        # If soft-delete column exists, mark deleted_at; otherwise remove the record
        if hasattr(category, 'deleted_at'):
            category.deleted_at = datetime.utcnow()
        else:
            db.session.delete(category)
        db.session.commit()
        
        return {'message': 'Category deleted successfully'}, 200

class SubcategoryListResource(Resource):
    def get(self):
        """Get all subcategories - Public access"""
        if hasattr(Subcategory, 'deleted_at'):
            subcategories = Subcategory.query.filter_by(deleted_at=None).all()
        else:
            subcategories = Subcategory.query.all()
        return [{
            'id': s.id,
            'category_id': s.category_id,
            'name': s.name,
            'description': s.description,
            'created_at': s.created_at.isoformat() if s.created_at else None
        } for s in subcategories]
    
    @require_role('admin')
    def post(self):
        """Create new subcategory - Admin only"""
        data = request.json
        
        if not data.get('name') or not data.get('category_id'):
            return {'error': 'Subcategory name and category_id are required'}, 400
        
        subcategory = Subcategory(
            category_id=data['category_id'],
            name=data['name'].strip(),
            description=data.get('description', '').strip()
        )
        
        db.session.add(subcategory)
        db.session.commit()
        
        return {
            'message': 'Subcategory created successfully',
            'subcategory': {
                'id': subcategory.id,
                'category_id': subcategory.category_id,
                'name': subcategory.name,
                'description': subcategory.description
            }
        }, 201

class SubcategoryResource(Resource):
    def get(self, subcategory_id):
        """Get subcategory details - Public access"""
        subcategory = Subcategory.query.get_or_404(subcategory_id)
        return {
            'id': subcategory.id,
            'category_id': subcategory.category_id,
            'name': subcategory.name,
            'description': subcategory.description,
            'created_at': subcategory.created_at.isoformat() if subcategory.created_at else None
        }
    
    @require_role('admin')
    def put(self, subcategory_id):
        """Update subcategory - Admin only"""
        subcategory = Subcategory.query.get_or_404(subcategory_id)
        data = request.json
        
        if 'name' in data:
            subcategory.name = data['name'].strip()
        if 'description' in data:
            subcategory.description = data['description'].strip()
        if 'category_id' in data:
            subcategory.category_id = data['category_id']
        
        db.session.commit()
        
        return {
            'message': 'Subcategory updated successfully',
            'subcategory': {
                'id': subcategory.id,
                'category_id': subcategory.category_id,
                'name': subcategory.name,
                'description': subcategory.description
            }
        }, 200
    
    @require_role('admin')
    def delete(self, subcategory_id):
        """Delete subcategory - Admin only"""
        subcategory = Subcategory.query.get_or_404(subcategory_id)
        from datetime import datetime
        if hasattr(subcategory, 'deleted_at'):
            subcategory.deleted_at = datetime.utcnow()
        else:
            db.session.delete(subcategory)
        db.session.commit()
        
        return {'message': 'Subcategory deleted successfully'}, 200

# Register routes
category_api.add_resource(CategoryListResource, '/')
category_api.add_resource(CategoryResource, '/<category_id>')
category_api.add_resource(SubcategoryListResource, '/subcategories/')
category_api.add_resource(SubcategoryResource, '/subcategories/<subcategory_id>')