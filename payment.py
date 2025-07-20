import threading
import random
from typing import Dict
from core.utilities import FileHandler
from core.exceptions import PaymentFailedError

class PaymentProcessor:
    def __init__(self):
        self._file_path = "data/payments.json"
        self._payments = FileHandler.read_json(self._file_path)
        self._lock = threading.Lock()
    
    def process_payment(self, order_id: str, amount: float, payment_method: Dict) -> str:
        payment_id = f"pay_{len(self._payments) + 1}"
        
        # Simulate payment processing with 10% failure rate
        is_success = random.random() > 0.1
        
        payment_data = {
            'id': payment_id,
            'order_id': order_id,
            'amount': amount,
            'method': payment_method,
            'status': 'completed' if is_success else 'failed',
            'processed_at': datetime.now().isoformat()
        }
        
        with self._lock:
            self._payments[payment_id] = payment_data
            FileHandler.write_json(self._file_path, self._payments)
        
        if not is_success:
            raise PaymentFailedError("Payment processing failed")
        
        return payment_id
    
    def issue_refund(self, payment_id: str) -> bool:
        with self._lock:
            if payment_id not in self._payments:
                raise PaymentFailedError(f"Payment {payment_id} not found")
            
            payment = self._payments[payment_id]
            payment['status'] = 'refunded'
            payment['refunded_at'] = datetime.now().isoformat()
            FileHandler.write_json(self._file_path, self._payments)
            
            return True