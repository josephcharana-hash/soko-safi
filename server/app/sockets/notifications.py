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


def get_notification_message(notification_type, data):
    """Get notification message based on type and data"""
    if notification_type == 'payment_success':
        return f"Your payment of KES {data.get('amount', 0)} for order {data.get('order_id', 'N/A')} was successful."
    elif notification_type == 'payment_failed':
        return f"Your payment for order {data.get('order_id', 'N/A')} failed: {data.get('reason', 'Unknown error')}"
    elif notification_type == 'disbursement_success':
        return f"You have received KES {data.get('amount', 0)} for your products."
    elif notification_type == 'disbursement_retry':
        return f"We're still processing your payment of KES {data.get('amount', 0)}. Next retry in {data.get('next_retry', 'N/A')}."
    elif notification_type == 'disbursement_failed':
        return f"There was an issue processing your payment. {data.get('message', 'Please contact support.')}"
    elif notification_type == 'order_status_change':
        return f"Your order {data.get('order_id', 'N/A')} status changed to {data.get('status', 'N/A')}."
    elif notification_type == 'new_message':
        return f"You have a new message from {data.get('sender_name', 'someone')}."

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