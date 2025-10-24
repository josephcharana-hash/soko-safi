from flask_restful import Resource, Api
from flask import Blueprint, request
from app.models import db, Review

review_bp = Blueprint('review_bp', __name__)
review_api = Api(review_bp)

class ProductReviewResource(Resource):
    def get(self, product_id):
        reviews = Review.query.filter_by(product_id=product_id).all()
        return [{
            'id': r.id,
            'rating': r.rating,
            'title': r.title,
            'body': r.body,
            'created_at': r.created_at.isoformat()
        } for r in reviews]

class ReviewListResource(Resource):
    def post(self):
        data = request.json
        review = Review(**data)
        db.session.add(review)
        db.session.commit()
        return {'id': review.id}, 201

review_api.add_resource(ProductReviewResource, '/products/<product_id>/reviews')
review_api.add_resource(ReviewListResource, '/')