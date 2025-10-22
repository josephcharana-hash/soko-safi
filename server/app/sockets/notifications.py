from datetime import datetime
from app.extensions import socketio, connected_users

def send_notification(user_id, notification_type, data):
    """Send real-time notification to user"""
    if user_id in connected_users:
        socketio.emit('notification', {
            'type': notification_type,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }, room=connected_users[user_id])

def notify_order_status_change(user_id, order_id, new_status):
    """Notify user of order status change"""
    send_notification(user_id, 'order_status', {
        'order_id': order_id,
        'status': new_status,
        'message': f'Your order #{order_id} status changed to {new_status}'
    })

def notify_payment_confirmation(user_id, payment_id, status):
    """Notify user of payment confirmation"""
    send_notification(user_id, 'payment', {
        'payment_id': payment_id,
        'status': status,
        'message': f'Payment #{payment_id} {status}'
    })