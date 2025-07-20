import threading
from typing import Dict, List
from core.utilities import FileHandler

class SearchEngine:
    def __init__(self):
        self._restaurants_file = "data/restaurants.json"
        self._index = None
        self._lock = threading.Lock()
        self._build_index()
    
    def _build_index(self):
        with self._lock:
            restaurants = FileHandler.read_json(self._restaurants_file)
            self._index = {
                'by_name': {},
                'by_cuisine': {},
                'by_location': {}
            }
            
            for rest_id, restaurant in restaurants.items():
                # Index by name
                for word in restaurant['name'].lower().split():
                    if word not in self._index['by_name']:
                        self._index['by_name'][word] = []
                    self._index['by_name'][word].append(rest_id)
                
                # Index by cuisine
                for cuisine in restaurant.get('cuisines', []):
                    if cuisine not in self._index['by_cuisine']:
                        self._index['by_cuisine'][cuisine] = []
                    self._index['by_cuisine'][cuisine].append(rest_id)
                
                # Index by location
                location = restaurant.get('location', '')
                if location not in self._index['by_location']:
                    self._index['by_location'][location] = []
                self._index['by_location'][location].append(rest_id)
    
    def search(self, query: str, filters: Dict = None) -> List[Dict]:
        with self._lock:
            restaurants = FileHandler.read_json(self._restaurants_file)
            
            # Simple search implementation - would use proper search engine in production
            query = query.lower()
            results = []
            
            # Search by name
            for word in query.split():
                if word in self._index['by_name']:
                    for rest_id in self._index['by_name'][word]:
                        if rest_id not in results:
                            results.append(rest_id)
            
            # Apply filters
            if filters:
                filtered_results = []
                for rest_id in results:
                    restaurant = restaurants[rest_id]
                    match = True
                    
                    if 'cuisine' in filters and filters['cuisine'] not in restaurant.get('cuisines', []):
                        match = False
                    if 'min_rating' in filters and restaurant.get('rating', 0) < filters['min_rating']:
                        match = False
                    if 'location' in filters and restaurant.get('location') != filters['location']:
                        match = False
                    
                    if match:
                        filtered_results.append(rest_id)
                
                results = filtered_results
            
            return [{'id': rid, **restaurants[rid]} for rid in results]