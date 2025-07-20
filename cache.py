import threading
import time
from typing import Any, Dict
import redis

class CacheManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CacheManager, cls).__new__(cls)
                cls._instance._init_cache()
            return cls._instance
    
    def _init_cache(self):
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        self.local_cache = {}
        self.local_cache_lock = threading.Lock()
    
    def get(self, key: str) -> Any:
        # Try local cache first
        with self.local_cache_lock:
            if key in self.local_cache:
                item = self.local_cache[key]
                if item['expiry'] > time.time():
                    return item['value']
                del self.local_cache[key]
        
        # Fall back to Redis
        value = self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        # Set in both caches
        serialized = json.dumps(value) if isinstance(value, (dict, list)) else value
        
        with self.local_cache_lock:
            self.local_cache[key] = {
                'value': value,
                'expiry': time.time() + ttl
            }
        
        return self.redis.setex(key, ttl, serialized)
    
    def invalidate(self, key: str) -> None:
        with self.local_cache_lock:
            if key in self.local_cache:
                del self.local_cache[key]
        
        self.redis.delete(key)