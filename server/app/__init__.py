from flask import Flask
from app.extensions import db, socketio

def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'your-secret-key'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soko_safi.db'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(flask_app)
    socketio.init_app(flask_app)
    
    # Import models to ensure they are registered
    from . import models
    
    # Import socket events (registers handlers)
    from . import sockets
    
    # Register route blueprints
    from routes.user_routes import user_bp
    from routes.product_routes import product_bp
    from routes.cart_routes import cart_bp
    from routes.category_routes import category_bp
    from routes.order_routes import order_bp
    from routes.payment_routes import payment_bp
    from routes.review_routes import review_bp
    from routes.message_routes import message_bp
    
    flask_app.register_blueprint(user_bp, url_prefix='/api/users')
    flask_app.register_blueprint(product_bp, url_prefix='/api/products')
    flask_app.register_blueprint(cart_bp, url_prefix='/api/cart')
    flask_app.register_blueprint(category_bp, url_prefix='/api/categories')
    flask_app.register_blueprint(order_bp, url_prefix='/api/orders')
    flask_app.register_blueprint(payment_bp, url_prefix='/api/payments')
    flask_app.register_blueprint(review_bp, url_prefix='/api/reviews')
    flask_app.register_blueprint(message_bp, url_prefix='/api/messages')
    
    # Routes
    @flask_app.route('/')
    def home():
        return "Yo! Flask is up and running 🔥 with WebSockets!"
    
    @flask_app.route('/test')
    def test_client():
        return flask_app.send_static_file('../test_client.html')
    
    # Test endpoints
    from .sockets.notifications import notify_order_status_change, notify_payment_confirmation
    
    @flask_app.route('/test/order/<int:user_id>/<int:order_id>/<status>')
    def test_order_notification(user_id, order_id, status):
        notify_order_status_change(user_id, order_id, status)
        return f'Order notification sent to user {user_id}'

    @flask_app.route('/test/payment/<int:user_id>/<int:payment_id>/<status>')
    def test_payment_notification(user_id, payment_id, status):
        notify_payment_confirmation(user_id, payment_id, status)
        return f'Payment notification sent to user {user_id}'
    
    return flask_app