import threading
from typing import List, Dict
from core.utilities import FileHandler

class RecommendationEngine:
    def __init__(self):
        self._orders_file = "data/orders.json"
        self._restaurants_file = "data/restaurants.json"
        self._users_file = "data/users.json"
        self._lock = threading.Lock()
    
    def get_personalized_recommendations(self, user_id: str, limit: int = 5) -> List[Dict]:
        with self._lock:
            orders = FileHandler.read_json(self._orders_file)
            restaurants = FileHandler.read_json(self._restaurants_file)
            
            # Get user's order history
            user_orders = [
                order for order in orders.values() 
                if order['user_id'] == user_id
            ]
            
            # Extract favorite cuisines
            cuisine_counts = {}
            for order in user_orders:
                restaurant = restaurants.get(order['restaurant_id'], {})
                for cuisine in restaurant.get('cuisines', []):
                    cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
            
            # Get top 3 favorite cuisines
            favorite_cuisines = sorted(
                cuisine_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            favorite_cuisines = [cuisine for cuisine, count in favorite_cuisines]
            
            # Recommend restaurants with similar cuisines
            recommendations = []
            for restaurant in restaurants.values():
                if any(cuisine in favorite_cuisines for cuisine in restaurant.get('cuisines', [])):
                    recommendations.append(restaurant)
            
            # Sort by rating and limit results
            recommendations.sort(key=lambda x: x.get('rating', 0), reverse=True)
            return recommendations[:limit]