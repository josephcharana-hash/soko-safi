from flask import Blueprint, request, jsonify
from models import db, Category

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in categories])

@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.json
    category = Category(**data)
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id}), 201