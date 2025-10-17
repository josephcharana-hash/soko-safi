from flask import Blueprint, jsonify, request
from models import db, Product

# Create Blueprint
product_bp = Blueprint("product_bp", __name__)

# ------------------------
# GET all products
# ------------------------
@product_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description
        } for p in products
    ]), 200


# ------------------------
# CREATE a new product
# ------------------------
@product_bp.route("/", methods=["POST"])
def create_product():
    data = request.get_json()
    product = Product(
        name=data["name"],
        price=data["price"],
        description=data.get("description", "")
    )

    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product created successfully"}), 201


# ------------------------
# GET a specific product by ID
# ------------------------
@product_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description
    }), 200


# ------------------------
# UPDATE a product
# ------------------------
@product_bp.route("/<int:id>", methods=["PATCH"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.description = data.get("description", product.description)

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200


# ------------------------
# DELETE a product
# ------------------------
@product_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200
