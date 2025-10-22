from flask_restful import Resource, Api
from flask import Blueprint, request
from models import db, User

user_bp = Blueprint('user_bp', __name__)
user_api = Api(user_bp)

class UserListResource(Resource):
    def get(self):
        users = User.query.filter_by(deleted_at=None).all()
        return [{
            'id': u.id,
            'role': u.role.value,
            'email': u.email,
            'full_name': u.full_name,
            'phone': u.phone,
            'location': u.location
        } for u in users]
    
    def post(self):
        data = request.json
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return {'id': user.id}, 201

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {
            'id': user.id,
            'role': user.role.value,
            'email': user.email,
            'full_name': user.full_name,
            'phone': user.phone,
            'location': user.location
        }

user_api.add_resource(UserListResource, '/')
user_api.add_resource(UserResource, '/<user_id>')