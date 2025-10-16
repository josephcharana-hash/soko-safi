from flask import Blueprint, jsonify, request
from server.models import User
# from server.routes.user_routes import user_bp
from server.models import db, User




user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(username=data["username"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@user_bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})

@user_bp.route("/<int:id>", methods=["PATCH"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@user_bp.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})
