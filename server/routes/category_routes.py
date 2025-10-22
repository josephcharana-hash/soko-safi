from flask_restful import Resource, Api
from flask import Blueprint, request
from models import db, Category

category_bp = Blueprint('category_bp', __name__)
category_api = Api(category_bp)

class CategoryListResource(Resource):
    def get(self):
        categories = Category.query.all()
        return [{
            'id': c.id,
            'name': c.name,
            'description': c.description
        } for c in categories]
    
    def post(self):
        data = request.json
        category = Category(**data)
        db.session.add(category)
        db.session.commit()
        return {'id': category.id}, 201

category_api.add_resource(CategoryListResource, '/')