import threading
from typing import Dict, List
from core.utilities import FileHandler
from core.exceptions import RestaurantNotFoundError

class RestaurantManager:
    def __init__(self):
        self._file_path = "data/restaurants.json"
        self._restaurants = FileHandler.read_json(self._file_path)
        self._lock = threading.Lock()
    
    def search_restaurants(self, query: str, filters: Dict = None) -> List[Dict]:
        with self._lock:
            results = []
            for rest_id, restaurant in self._restaurants.items():
                if query.lower() in restaurant['name'].lower():
                    if filters and not self._matches_filters(restaurant, filters):
                        continue
                    results.append({'id': rest_id, **restaurant})
            return results
    
    def _matches_filters(self, restaurant: Dict, filters: Dict) -> bool:
        for key, value in filters.items():
            if key == 'cuisine' and value not in restaurant['cuisines']:
                return False
            if key == 'min_rating' and restaurant['rating'] < value:
                return False
        return True
    
    def update_inventory(self, restaurant_id: str, item_id: str, quantity: int) -> None:
        with self._lock:
            if restaurant_id not in self._restaurants:
                raise RestaurantNotFoundError(f"Restaurant {restaurant_id} not found")
            
            menu = self._restaurants[restaurant_id]['menu']
            for item in menu:
                if item['id'] == item_id:
                    item['quantity'] = max(0, item['quantity'] - quantity)
                    break
            
            FileHandler.write_json(self._file_path, self._restaurants)