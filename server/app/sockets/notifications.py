from datetime import datetime
import json
from app.extensions import socketio, connected_users, db

def send_notification(user_id, notification_type, data):
    """Send real-time notification to user via WebSocket"""
    try:
        # Send via WebSocket if user is connected
        if user_id in connected_users:
            socketio.emit('notification', {
                'type': notification_type,
                'data': data,
                'timestamp': datetime.utcnow().isoformat()
            }, room=connected_users[user_id])

        # Also create database notification record
        from app.models import Notification, NotificationType
        notification = Notification(
            user_id=user_id,
            type=get_notification_type_enum(notification_type),
            title=get_notification_title(notification_type),
            message=get_notification_message(notification_type, data),
            data=json.dumps(data)
        )
        db.session.add(notification)
        db.session.commit()

    except Exception as e:
        print(f"Failed to send notification: {str(e)}")


def get_notification_type_enum(notification_type):
    """Map notification type to enum"""
    from app.models import NotificationType
    type_mapping = {
        'payment_success': NotificationType.info,
        'payment_failed': NotificationType.error,
        'disbursement_success': NotificationType.success,
        'disbursement_retry': NotificationType.warning,
        'disbursement_failed': NotificationType.error,
        'order_status_change': NotificationType.info,
        'new_message': NotificationType.info
    }
    return type_mapping.get(notification_type, NotificationType.info)


def get_notification_title(notification_type):
    """Get notification title based on type"""
    titles = {
        'payment_success': 'Payment Successful',
        'payment_failed': 'Payment Failed',
        'disbursement_success': 'Payment Received',
        'disbursement_retry': 'Payment Processing',
        'disbursement_failed': 'Payment Issue',
        'order_status_change': 'Order Update',
        'new_message': 'New Message'
    }
    return titles.get(notification_type, 'Notification')


def sanitize_text(text):
    """Sanitize text to prevent XSS"""
    if not text:
        return 'N/A'
    return str(text).replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')

def get_notification_message(notification_type, data):
    """Get notification message based on type and data"""
    if notification_type == 'payment_success':
        amount = sanitize_text(data.get('amount', 0))
        order_id = sanitize_text(data.get('order_id', 'N/A'))
        return f"Your payment of KES {amount} for order {order_id} was successful."
    elif notification_type == 'payment_failed':
        order_id = sanitize_text(data.get('order_id', 'N/A'))
        reason = sanitize_text(data.get('reason', 'Unknown error'))
        return f"Your payment for order {order_id} failed: {reason}"
    elif notification_type == 'disbursement_success':
        amount = sanitize_text(data.get('amount', 0))
        return f"You have received KES {amount} for your products."
    elif notification_type == 'disbursement_retry':
        amount = sanitize_text(data.get('amount', 0))
        next_retry = sanitize_text(data.get('next_retry', 'N/A'))
        return f"We're still processing your payment of KES {amount}. Next retry in {next_retry}."
    elif notification_type == 'disbursement_failed':
        message = sanitize_text(data.get('message', 'Please contact support.'))
        return f"There was an issue processing your payment. {message}"
    elif notification_type == 'order_status_change':
        order_id = sanitize_text(data.get('order_id', 'N/A'))
        status = sanitize_text(data.get('status', 'N/A'))
        return f"Your order {order_id} status changed to {status}."
    elif notification_type == 'new_message':
        sender_name = sanitize_text(data.get('sender_name', 'someone'))
        return f"You have a new message from {sender_name}."

    return "You have a new notification."


def notify_order_status_change(user_id, order_id, new_status):
    """Notify user of order status change"""
    send_notification(user_id, 'order_status_change', {
        'order_id': order_id,
        'status': new_status
    })

def notify_payment_confirmation(user_id, payment_id, status):
    """Notify user of payment confirmation"""
    send_notification(user_id, 'payment_success' if status == 'success' else 'payment_failed', {
        'payment_id': payment_id,
        'status': status
    })