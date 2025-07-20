import threading
from typing import Dict, List
from core.utilities import FileHandler
from core.exceptions import RestaurantNotFoundError

class InventoryManager:
    def __init__(self):
        self._restaurants_file = "data/restaurants.json"
        self._lock = threading.Lock()
    
    def update_inventory(self, restaurant_id: str, item_id: str, quantity: int) -> bool:
        with self._lock:
            restaurants = FileHandler.read_json(self._restaurants_file)
            
            if restaurant_id not in restaurants:
                raise RestaurantNotFoundError(f"Restaurant {restaurant_id} not found")
            
            menu = restaurants[restaurant_id]['menu']
            for item in menu:
                if item['id'] == item_id:
                    item['quantity'] = max(0, item['quantity'] - quantity)
                    break
            
            FileHandler.write_json(self._restaurants_file, restaurants)
            return True
    
    def check_availability(self, restaurant_id: str, items: List[Dict]) -> bool:
        with self._lock:
            restaurants = FileHandler.read_json(self._restaurants_file)
            
            if restaurant_id not in restaurants:
                raise RestaurantNotFoundError(f"Restaurant {restaurant_id} not found")
            
            menu_items = {item['id']: item for item in restaurants[restaurant_id]['menu']}
            
            for order_item in items:
                menu_item = menu_items.get(order_item['id'])
                if not menu_item or menu_item['quantity'] < order_item['quantity']:
                    return False
            
            return True