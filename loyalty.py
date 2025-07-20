import threading
from typing import Dict
from core.utilities import FileHandler

class LoyaltyManager:
    def __init__(self):
        self._file_path = "data/loyalty.json"
        self._loyalty_data = FileHandler.read_json(self._file_path)
        self._lock = threading.Lock()
    
    def add_points(self, user_id: str, order_id: str, amount: float) -> int:
        points = int(amount)  # 1 point per rupee spent
        
        with self._lock:
            if user_id not in self._loyalty_data:
                self._loyalty_data[user_id] = {
                    'points': 0,
                    'transactions': []
                }
            
            self._loyalty_data[user_id]['points'] += points
            self._loyalty_data[user_id]['transactions'].append({
                'order_id': order_id,
                'points': points,
                'date': datetime.now().isoformat()
            })
            
            FileHandler.write_json(self._file_path, self._loyalty_data)
            
            return self._loyalty_data[user_id]['points']
    
    def redeem_points(self, user_id: str, points: int) -> bool:
        with self._lock:
            if user_id not in self._loyalty_data:
                return False
            
            if self._loyalty_data[user_id]['points'] < points:
                return False
            
            self._loyalty_data[user_id]['points'] -= points
            self._loyalty_data[user_id]['transactions'].append({
                'type': 'redemption',
                'points': -points,
                'date': datetime.now().isoformat()
            })
            
            FileHandler.write_json(self._file_path, self._loyalty_data)
            
            return True