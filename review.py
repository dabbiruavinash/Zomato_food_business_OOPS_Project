import threading
from typing import Dict, List
from core.utilities import FileHandler

class ReviewManager:
    def __init__(self):
        self._file_path = "data/reviews.json"
        self._reviews = FileHandler.read_json(self._file_path)
        self._lock = threading.Lock()
    
    def add_review(self, user_id: str, restaurant_id: str, rating: int, comment: str = "") -> str:
        review_id = f"review_{len(self._reviews) + 1}"
        
        review_data = {
            'id': review_id,
            'user_id': user_id,
            'restaurant_id': restaurant_id,
            'rating': rating,
            'comment': comment,
            'date': datetime.now().isoformat()
        }
        
        with self._lock:
            self._reviews[review_id] = review_data
            FileHandler.write_json(self._file_path, self._reviews)
        
        # Update restaurant average rating in background
        threading.Thread(
            target=self._update_restaurant_rating,
            args=(restaurant_id,)
        ).start()
        
        return review_id
    
    def _update_restaurant_rating(self, restaurant_id: str):
        with self._lock:
            reviews = FileHandler.read_json(self._file_path)
            restaurant_reviews = [
                r for r in reviews.values() 
                if r['restaurant_id'] == restaurant_id
            ]
            
            if not restaurant_reviews:
                return
            
            avg_rating = sum(r['rating'] for r in restaurant_reviews) / len(restaurant_reviews)
            
            restaurants = FileHandler.read_json("data/restaurants.json")
            if restaurant_id in restaurants:
                restaurants[restaurant_id]['rating'] = round(avg_rating, 1)
                FileHandler.write_json("data/restaurants.json", restaurants)