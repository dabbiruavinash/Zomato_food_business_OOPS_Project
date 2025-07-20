import threading
from typing import Dict
from core.utilities import FileHandler
from datetime import datetime, timedelta

class DiscountManager:
    def __init__(self):
        self._file_path = "data/discounts.json"
        self._discounts = FileHandler.read_json(self._file_path)
        self._lock = threading.Lock()
    
    def validate_coupon(self, coupon_code: str, user_id: str, order_amount: float) -> Dict:
        with self._lock:
            if coupon_code not in self._discounts:
                return {'valid': False, 'message': 'Invalid coupon code'}
            
            coupon = self._discounts[coupon_code]
            
            # Check expiration
            if datetime.now().isoformat() > coupon['expires_at']:
                return {'valid': False, 'message': 'Coupon expired'}
            
            # Check minimum order amount
            if order_amount < coupon['min_order_amount']:
                return {
                    'valid': False,
                    'message': f"Minimum order amount {coupon['min_order_amount']} required"
                }
            
            # Check user restrictions
            if coupon['user_specific'] and user_id not in coupon['allowed_users']:
                return {'valid': False, 'message': 'Coupon not valid for this user'}
            
            # Check usage limits
            if coupon['usage_limit'] <= coupon['times_used']:
                return {'valid': False, 'message': 'Coupon usage limit reached'}
            
            return {
                'valid': True,
                'discount_type': coupon['discount_type'],
                'discount_value': coupon['discount_value'],
                'message': 'Coupon applied successfully'
            }
    
    def apply_coupon(self, coupon_code: str) -> bool:
        with self._lock:
            if coupon_code not in self._discounts:
                return False
            
            self._discounts[coupon_code]['times_used'] += 1
            FileHandler.write_json(self._file_path, self._discounts)
            return True