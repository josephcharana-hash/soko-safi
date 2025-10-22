from flask import Blueprint, request, jsonify
from models import db, User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'role': user.role.value,
        'email': user.email,
        'full_name': user.full_name,
        'phone': user.phone,
        'location': user.location
    })