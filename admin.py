import threading
from typing import Dict, List
from core.utilities import FileHandler

class AdminManager:
    def __init__(self):
        self._restaurants_file = "data/restaurants.json"
        self._orders_file = "data/orders.json"
        self._users_file = "data/users.json"
        self._lock = threading.Lock()
    
    def get_system_stats(self) -> Dict:
        with self._lock:
            restaurants = FileHandler.read_json(self._restaurants_file)
            orders = FileHandler.read_json(self._orders_file)
            users = FileHandler.read_json(self._users_file)
            
            today = datetime.now().date().isoformat()
            today_orders = [
                o for o in orders.values() 
                if o['created_at'].startswith(today)
            ]
            
            return {
                'total_restaurants': len(restaurants),
                'total_users': len(users),
                'total_orders': len(orders),
                'today_orders': len(today_orders),
                'today_revenue': sum(
                    sum(item['price'] * item['quantity'] for item in o['items'])
                    for o in today_orders
                )
            }
    
    def get_flagged_orders(self) -> List[Dict]:
        with self._lock:
            orders = FileHandler.read_json(self._orders_file)
            return [
                o for o in orders.values() 
                if o.get('flags') and o['status'] != 'cancelled'
            ]
    
    def approve_restaurant(self, restaurant_id: str) -> bool:
        with self._lock:
            restaurants = FileHandler.read_json(self._restaurants_file)
            
            if restaurant_id not in restaurants:
                return False
            
            restaurants[restaurant_id]['approved'] = True
            restaurants[restaurant_id]['approved_at'] = datetime.now().isoformat()
            FileHandler.write_json(self._restaurants_file, restaurants)
            
            return True