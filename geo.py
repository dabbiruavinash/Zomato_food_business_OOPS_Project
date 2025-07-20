import threading
import math
from typing import Dict, Tuple
from core.utilities import FileHandler

class GeoService:
    EARTH_RADIUS_KM = 6371
    
    def __init__(self):
        self._restaurants_file = "data/restaurants.json"
        self._lock = threading.Lock()
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        # Convert degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return self.EARTH_RADIUS_KM * c
    
    def find_nearest_restaurants(self, user_lat: float, user_lon: float, limit: int = 5) -> list:
        with self._lock:
            restaurants = FileHandler.read_json(self._restaurants_file)
            
            # Calculate distances to all restaurants
            distances = []
            for rest_id, restaurant in restaurants.items():
                rest_lat = restaurant['location']['lat']
                rest_lon = restaurant['location']['lon']
                distance = self.calculate_distance(user_lat, user_lon, rest_lat, rest_lon)
                distances.append((distance, rest_id, restaurant))
            
            # Sort by distance and return top results
            distances.sort(key=lambda x: x[0])
            return [{
                'restaurant_id': rest_id,
                'name': restaurant['name'],
                'distance_km': round(distance, 2),
                'cuisines': restaurant['cuisines'],
                'rating': restaurant['rating']
            } for distance, rest_id, restaurant in distances[:limit]]
    
    def estimate_delivery_time(self, restaurant_location: Dict, user_location: Dict) -> int:
        # Simple estimation - would use more sophisticated algorithm in production
        distance = self.calculate_distance(
            restaurant_location['lat'],
            restaurant_location['lon'],
            user_location['lat'],
            user_location['lon']
        )
        
        # Assume average delivery speed of 20 km/h plus 15 minutes preparation time
        return round(15 + (distance / 20 * 60))