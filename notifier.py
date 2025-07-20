import smtplib
import threading
from email.mime.text import MIMEText
from typing import Dict

class NotificationService:
    def __init__(self):
        self._email_config = {
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'sender_email': 'noreply@zomato.com',
            'sender_password': 'password'
        }
        self._lock = threading.Lock()
    
    def send_email(self, recipient: str, subject: str, body: str) -> None:
        with self._lock:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self._email_config['sender_email']
            msg['To'] = recipient
            
            try:
                with smtplib.SMTP(
                    self._email_config['smtp_server'],
                    self._email_config['smtp_port']
                ) as server:
                    server.starttls()
                    server.login(
                        self._email_config['sender_email'],
                        self._email_config['sender_password']
                    )
                    server.send_message(msg)
            except Exception as e:
                print(f"Failed to send email: {str(e)}")
    
    def send_order_confirmation(self, user_id: str, order_id: str) -> None:
        # In a real app, would fetch user email from database
        email = f"{user_id}@example.com"
        subject = f"Your Zomato Order #{order_id} is confirmed"
        body = f"Thank you for your order! Your order ID is {order_id}."
        
        self.send_email(email, subject, body)
    
    def send_delivery_update(self, user_id: str, order_id: str, status: str) -> None:
        email = f"{user_id}@example.com"
        subject = f"Update on your Zomato Order #{order_id}"
        body = f"Your order status has been updated to: {status}"
        
        self.send_email(email, subject, body)