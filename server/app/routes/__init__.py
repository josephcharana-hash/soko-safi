from .user_routes import user_bp
from .product_routes import product_bp
from .order_routes import order_bp
from .cart_routes import cart_bp
from .category_routes import category_bp
from .review_routes import review_bp
from .message_routes import message_bp
from .payment_routes import payment_bp
from .favorite_routes import favorite_bp

def register_blueprints(app):
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')
    app.register_blueprint(message_bp, url_prefix='/api/messages')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(favorite_bp, url_prefix='/api/favorites')