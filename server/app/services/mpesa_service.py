"""
M-Pesa integration service for Soko Safi
Handles STK Push, B2C disbursements, and callback processing
"""

import os
import requests
import base64
import json
from datetime import datetime, timedelta
import time
from flask import current_app
from app.models import db, Payment, PaymentStatus, ArtisanDisbursement, DisbursementStatus, User
from app.sockets.notifications import send_notification


class MpesaService:
    def __init__(self):
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        self.shortcode = os.getenv('MPESA_SHORTCODE')
        self.passkey = os.getenv('MPESA_PASSKEY')
        self.base_url = os.getenv('MPESA_BASE_URL', 'https://sandbox.safaricom.co.ke')
        
        # Validate required credentials
        if not all([self.consumer_key, self.consumer_secret, self.shortcode, self.passkey]):
            raise ValueError('Missing required M-Pesa credentials in environment variables')
 
    def get_access_token(self):
        """Get M-Pesa access token"""
        try:
            if not self.consumer_key or not self.consumer_secret:
                raise ValueError('M-Pesa credentials not configured')
                
            auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
            headers = {
                'Authorization': f'Basic {auth}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials', headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()['access_token']
        except Exception as e:
            current_app.logger.error(f"Failed to get M-Pesa access token: {str(e)}")
            raise

    def initiate_stk_push(self, phone_number, amount, order_id, account_reference):
        """Initiate STK Push for customer payment"""
        try:
            access_token = self.get_access_token()
            # Format phone number (remove + and ensure 254 format)
            phone = phone_number.replace('+', '')
            if phone.startswith('0'):
                phone = '254' + phone[1:]
            elif not phone.startswith('254'):
                phone = '254' + phone

            # Generate timestamp and password 
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()

            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone,
                "PartyB": self.shortcode,
                "PhoneNumber": phone,
                "CallBackURL": f"{os.getenv('BASE_URL', 'http://localhost:5001')}/api/payments/callback",
                "AccountReference": account_reference,
                "TransactionDesc": f"Payment for Order {order_id}"
            }

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(f'{self.base_url}/mpesa/stkpush/v1/processrequest', json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()
            return {
                'success': True,
                'checkout_request_id': result.get('CheckoutRequestID'),
                'response_code': result.get('ResponseCode'),
                'response_description': result.get('ResponseDescription'),
                'customer_message': result.get('CustomerMessage')
            }

        except Exception as e:
            current_app.logger.error(f"STK Push failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def disburse_to_artisan(self, disbursement_id):
        """Disburse payment to artisan via B2C"""
        try:
            disbursement = ArtisanDisbursement.query.get(disbursement_id)
            if not disbursement:
                raise ValueError("Disbursement not found")

            artisan = User.query.get(disbursement.artisan_id)
            if not artisan:
                raise ValueError("Artisan not found")

            access_token = self.get_access_token()

            # Determine recipient based on payment method
            if disbursement.disbursement_method == 'phone':
                recipient = disbursement.recipient_phone.replace('+', '')
                if recipient.startswith('0'):
                    recipient = '254' + recipient[1:]
            else:  # paybill
                recipient = disbursement.paybill_number

            payload = {
                "InitiatorName": os.getenv('MPESA_INITIATOR_NAME', 'testapi'),
                "SecurityCredential": os.getenv('MPESA_SECURITY_CREDENTIAL', 'Safaricom999!*!'),
                "CommandID": "BusinessPayment",
                "Amount": int(disbursement.amount),
                "PartyA": self.shortcode,
                "PartyB": recipient,
                "Remarks": f"Payment for order items",
                "QueueTimeOutURL": f"{os.getenv('BASE_URL', 'http://localhost:5001')}/api/payments/b2c/timeout",
                "ResultURL": f"{os.getenv('BASE_URL', 'http://localhost:5001')}/api/payments/b2c/result",
                "Occasion": f"Order {disbursement.payment_id}"
            }

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(f'{self.base_url}/mpesa/b2c/v1/paymentrequest', json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()
            return {
                'success': True,
                'conversation_id': result.get('ConversationID'),
                'originator_conversation_id': result.get('OriginatorConversationID'),
                'response_code': result.get('ResponseCode'),
                'response_description': result.get('ResponseDescription')
            }

        except Exception as e:
            current_app.logger.error(f"B2C disbursement failed: {str(e)}")
            return {'success': False, 'error': str(e)}

    def process_stk_callback(self, callback_data):
        """Process STK Push callback"""
        try:
            result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            result_desc = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultDesc')
            checkout_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
            callback_metadata = callback_data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {})

            # Find payment by checkout request ID (you'll need to store this mapping) 
            payment = Payment.query.filter_by(mpesa_transaction_id=checkout_request_id).first()
            if not payment:
                current_app.logger.error(f"Payment not found for checkout_request_id: {checkout_request_id}")
                return

            if result_code == 0:
                # Success
                payment.status = PaymentStatus.success
                payment.mpesa_transaction_id = callback_metadata.get('Item', [{}])[1].get('Value')  # MpesaReceiptNumber
                payment.received_at = datetime.utcnow()
                payment.callback_payload = callback_data

                # Trigger artisan disbursements
                self._trigger_artisan_disbursements(payment.id)

                # Notify user via WebSocket
                send_notification(payment.order.user_id, 'payment_success', {
                    'order_id': payment.order_id,
                    'amount': float(payment.amount),
                    'transaction_id': payment.mpesa_transaction_id
                })

            else:
                # Failed
                payment.status = PaymentStatus.failed
                payment.transaction_status_reason = result_desc
                payment.callback_payload = json.dumps(callback_data) 

                # Notify user of failure
                send_notification(payment.order.user_id, 'payment_failed', {
                    'order_id': payment.order_id,
                    'amount': float(payment.amount),
                    'reason': result_desc
                })

            db.session.commit()

        except Exception as e:
            current_app.logger.error(f"STK callback processing failed: {str(e)}") 
            db.session.rollback()

    def process_b2c_result(self, result_data):
        """Process B2C result callback"""
        try:
            result_code = result_data.get('Result', {}).get('ResultCode')
            result_desc = result_data.get('Result', {}).get('ResultDesc')
            transaction_id = result_data.get('Result', {}).get('TransactionId')
            conversation_id = result_data.get('Result', {}).get('ConversationId') 

            # Find disbursement by conversation ID (you'll need to store this mapping)
            disbursement = ArtisanDisbursement.query.filter_by(mpesa_transaction_id=conversation_id).first()
            if not disbursement:
                current_app.logger.error(f"Disbursement not found for conversation_id: {conversation_id}")
                return

            if result_code == 0:
                # Success
                disbursement.status = DisbursementStatus.success
                disbursement.mpesa_transaction_id = transaction_id
                disbursement.completed_at = datetime.utcnow()
                disbursement.callback_payload = json.dumps(result_data) 

                # Notify artisan
                send_notification(disbursement.artisan_id, 'disbursement_success', {
                    'amount': float(disbursement.amount),
                    'transaction_id': transaction_id
                })

            else:
                # Failed - implement retry logic
                disbursement.failure_reason = result_desc
                disbursement.callback_payload = json.dumps(result_data) 
                self._handle_disbursement_failure(disbursement)

            db.session.commit()

        except Exception as e:
            current_app.logger.error(f"B2C result processing failed: {str(e)}") 
            db.session.rollback()

    def _trigger_artisan_disbursements(self, payment_id):
        """Create and trigger disbursements to artisans"""
        try:
            payment = Payment.query.get(payment_id)
            order_items = payment.order.order_items

            # Group by artisan
            artisan_totals = {}
            for item in order_items:
                artisan_id = item.artisan_id
                if artisan_id not in artisan_totals:
                    artisan_totals[artisan_id] = 0
                artisan_totals[artisan_id] += float(item.total_price)

            # Create disbursements
            for artisan_id, amount in artisan_totals.items():
                artisan = User.query.get(artisan_id)

                disbursement = ArtisanDisbursement(
                    payment_id=payment_id,
                    artisan_id=artisan_id,
                    amount=amount,
                    disbursement_method=artisan.payment_method.value if artisan.payment_method else 'phone',
                    recipient_phone=artisan.mpesa_phone,
                    paybill_number=artisan.paybill_number,
                    paybill_account=artisan.paybill_account
                )

                db.session.add(disbursement)
                db.session.commit()

                # Trigger disbursement 
                result = self.disburse_to_artisan(disbursement.id)
                if result['success']:
                    disbursement.status = DisbursementStatus.processing
                    disbursement.mpesa_transaction_id = result.get('conversation_id')
                else:
                    disbursement.status = DisbursementStatus.failed 
                    disbursement.failure_reason = result.get('error')

                db.session.commit()

        except Exception as e:
            current_app.logger.error(f"Failed to trigger artisan disbursements: {str(e)}") 
            db.session.rollback()

    def _handle_disbursement_failure(self, disbursement):
        """Handle failed disbursement with retry logic"""
        try:
            disbursement.retry_count += 1
            disbursement.last_retry_at = datetime.utcnow() 

            if disbursement.retry_count < 5:
                # Schedule retry with exponential backoff
                retry_delays = [300, 900, 3600, 21600, 86400]  # 5min, 15min, 1hr, 6hr, 24hr
                delay = retry_delays[disbursement.retry_count - 1]

                # In a real implementation, you'd use a task queue like Celery
                # For now, we'll mark as retry and log
                disbursement.status = DisbursementStatus.retry
                current_app.logger.info(f"Disbursement {disbursement.id} scheduled for retry in {delay} seconds")

                # Notify artisan of retry
                send_notification(disbursement.artisan_id, 'disbursement_retry', {
                    'amount': float(disbursement.amount),
                    'retry_count': disbursement.retry_count,
                    'next_retry': (datetime.utcnow() + timedelta(seconds=delay)).isoformat() 
                })

            else:
                # Max retries reached - manual intervention required
                disbursement.status = DisbursementStatus.manual

                # Notify artisan and admin
                send_notification(disbursement.artisan_id, 'disbursement_failed', {
                    'amount': float(disbursement.amount),
                    'reason': disbursement.failure_reason,
                    'message': 'Payment disbursement failed. Please contact support.'
                })

                # TODO: Notify admin for manual processing

        except Exception as e:
            current_app.logger.error(f"Failed to handle disbursement failure: {str(e)}") 


# Global service instance
mpesa_service = MpesaService()