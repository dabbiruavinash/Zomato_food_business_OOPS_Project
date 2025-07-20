import threading
from typing import Dict, List
from core.utilities import FileHandler
from core.exceptions import UserNotFoundError

class UserManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(UserManager, cls).__new__(cls)
                cls._instance._init()
            return cls._instance
    
    def _init(self):
        self._file_path = "data/users.json"
        self._users = FileHandler.read_json(self._file_path)
        self._lock = threading.Lock()
    
    def get_user(self, user_id: str) -> Dict:
        with self._lock:
            user = self._users.get(user_id)
            if not user:
                raise UserNotFoundError(f"User {user_id} not found")
            return user
    
    def add_user(self, user_data: Dict) -> str:
        with self._lock:
            user_id = f"user_{len(self._users) + 1}"
            self._users[user_id] = user_data
            FileHandler.write_json(self._file_path, self._users)
            return user_id
    
    def update_user(self, user_id: str, updates: Dict) -> None:
        with self._lock:
            if user_id not in self._users:
                raise UserNotFoundError(f"User {user_id} not found")
            self._users[user_id].update(updates)
            FileHandler.write_json(self._file_path, self._users)