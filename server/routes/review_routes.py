from flask import Blueprint, request, jsonify
from models import db, Review

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/products/<product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([{
        'id': r.id,
        'rating': r.rating,
        'title': r.title,
        'body': r.body,
        'created_at': r.created_at.isoformat()
    } for r in reviews])

@review_bp.route('/', methods=['POST'])
def create_review():
    data = request.json
    review = Review(**data)
    db.session.add(review)
    db.session.commit()
    return jsonify({'id': review.id}), 201