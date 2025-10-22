from flask import Flask
from app.extensions import db, socketio

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soko_safi.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    
    # Import models
    from app.models import message
    
    # Import socket events (registers handlers)
    from app import sockets
    
    # Routes
    @app.route('/')
    def home():
        return "Yo! Flask is up and running 🔥 with WebSockets!"
    
    @app.route('/test')
    def test_client():
        return app.send_static_file('../test_client.html')
    
    # Test endpoints
    from app.sockets.notifications import notify_order_status_change, notify_payment_confirmation
    
    @app.route('/test/order/<int:user_id>/<int:order_id>/<status>')
    def test_order_notification(user_id, order_id, status):
        notify_order_status_change(user_id, order_id, status)
        return f'Order notification sent to user {user_id}'

    @app.route('/test/payment/<int:user_id>/<int:payment_id>/<status>')
    def test_payment_notification(user_id, payment_id, status):
        notify_payment_confirmation(user_id, payment_id, status)
        return f'Payment notification sent to user {user_id}'
    
    return app