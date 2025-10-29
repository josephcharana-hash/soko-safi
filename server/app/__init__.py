import os
from flask import Flask
from app.extensions import db, socketio, session
from dotenv import load_dotenv

load_dotenv()

def create_app():
    flask_app = Flask(__name__)
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        raise ValueError('SECRET_KEY environment variable is required')
    flask_app.config['SECRET_KEY'] = secret_key
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Session configuration
    flask_app.config['SESSION_TYPE'] = 'filesystem'
    flask_app.config['SESSION_PERMANENT'] = False
    flask_app.config['SESSION_USE_SIGNER'] = True
    flask_app.config['SESSION_KEY_PREFIX'] = 'soko_safi:'
    flask_app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'instance', 'sessions')
    flask_app.config['SESSION_FILE_THRESHOLD'] = 500
    flask_app.config['UPLOAD_FOLDER'] = os.path.join(flask_app.root_path, 'uploads')
    flask_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Initialize extensions
    db.init_app(flask_app)
    session.init_app(flask_app)
    # Enable CORS for API routes and allow credentials (cookies/session)
    from .extensions import cors, socketio
    cors.init_app(flask_app, resources={
        r"/api/*": {
            "origins": ["*", "http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    }, supports_credentials=True)
    socketio.init_app(flask_app)
    
    # Import models to ensure they are registered
    from . import models
    
    # Import socket events (registers handlers)
    from . import sockets
    
    # Register route blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.product_routes import product_bp
    from app.routes.cart_routes import cart_bp
    from app.routes.category_routes import category_bp
    from app.routes.order_routes import order_bp
    from app.routes.payment_routes import payment_bp
    from app.routes.review_routes import review_bp
    from app.routes.message_routes import message_bp
    from app.routes.favorite_routes import favorite_bp
    from app.routes.follow_routes import follow_bp
    from app.routes.notification_routes import notification_bp
    from app.routes.artisan_routes import artisan_bp
    from app.routes.upload_routes import upload_bp
    from app.routes.collection_routes import collection_bp
    
    flask_app.register_blueprint(auth_bp, url_prefix='/api/auth')
    flask_app.register_blueprint(user_bp, url_prefix='/api/users')
    flask_app.register_blueprint(product_bp, url_prefix='/api/products')
    flask_app.register_blueprint(cart_bp, url_prefix='/api/cart')
    flask_app.register_blueprint(category_bp, url_prefix='/api/categories')
    flask_app.register_blueprint(order_bp, url_prefix='/api/orders')
    flask_app.register_blueprint(payment_bp, url_prefix='/api/payments')
    flask_app.register_blueprint(review_bp, url_prefix='/api/reviews')
    flask_app.register_blueprint(message_bp, url_prefix='/api/messages')
    flask_app.register_blueprint(favorite_bp, url_prefix='/api/favorites')
    flask_app.register_blueprint(follow_bp, url_prefix='/api/follows')
    flask_app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    flask_app.register_blueprint(artisan_bp, url_prefix='/api/artisan')
    flask_app.register_blueprint(upload_bp, url_prefix='/api/upload')
    flask_app.register_blueprint(collection_bp, url_prefix='/api/collections')
    
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
        # Sanitize status to prevent XSS
        safe_status = str(status).replace('<', '&lt;').replace('>', '&gt;')
        notify_order_status_change(user_id, order_id, safe_status)
        return f'Order notification sent to user {user_id}'

    @flask_app.route('/test/payment/<int:user_id>/<int:payment_id>/<status>')
    def test_payment_notification(user_id, payment_id, status):
        # Sanitize status to prevent XSS
        safe_status = str(status).replace('<', '&lt;').replace('>', '&gt;')
        notify_payment_confirmation(user_id, payment_id, safe_status)
        return f'Payment notification sent to user {user_id}'
    
    return flask_app