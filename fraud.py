import threading
from typing import Dict
from core.utilities import FileHandler
from datetime import datetime, timedelta

class FraudDetector:
    def __init__(self):
        self._orders_file = "data/orders.json"
        self._users_file = "data/users.json"
        self._lock = threading.Lock()
    
    def analyze_order(self, order_data: Dict) -> Dict:
        with self._lock:
            orders = FileHandler.read_json(self._orders_file)
            users = FileHandler.read_json(self._users_file)
            
            user_id = order_data['user_id']
            risk_score = 0
            flags = []
            
            # Check for new user
            if user_id not in users:
                risk_score += 20
                flags.append('new_user')
            
            # Check for high-value order
            order_value = sum(item['price'] * item['quantity'] for item in order_data['items'])
            if order_value > 2000:  # Threshold for high-value orders
                risk_score += 15
                flags.append('high_value_order')
            
            # Check for multiple recent orders
            user_orders = [o for o in orders.values() if o['user_id'] == user_id]
            last_hour_orders = [
                o for o in user_orders 
                if datetime.fromisoformat(o['created_at']) > datetime.now() - timedelta(hours=1)
            ]
            
            if len(last_hour_orders) > 3:
                risk_score += 25
                flags.append('multiple_orders_in_short_time')
            
            # Check for unusual delivery location
            if 'delivery_location' in order_data:
                user = users.get(user_id, {})
                if 'usual_locations' in user:
                    if order_data['delivery_location'] not in user['usual_locations']:
                        risk_score += 30
                        flags.append('unusual_delivery_location')
            
            return {
                'risk_score': min(risk_score, 100),
                'flags': flags,
                'recommendation': 'review' if risk_score > 50 else 'approve'
            }