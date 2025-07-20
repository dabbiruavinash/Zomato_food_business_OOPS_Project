import json
import logging
from pathlib import Path
from typing import Dict,List,Any
from datetime import datetime

class FileHandler:
       @staticmethod
       def read_json(file_path: str) -> Dic[str, Any]:
              try:
                   with open(file_path,'r') as f:
                         return json.load(f)
              except (FileNotFoundError, json.JSONecodeError) as e:
                    logging.error(f"Error reading file {file_path} : {str(e)}")
                    raise

        @staticmethod
        def write_json(file_path:str, data: Dict[str, Any]) -> None:
               try:
                    with open(file_path, 'w') as f:
                            json.dump(data, f, indent=4)
               except IOError as e:
                     logging.error(f"Error wrtiting to file {file_path} : {str(e)}")
                     raise

class ThreadSafeLogger:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, log_file: str = "app.log"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ThreadSafeLogger, cls).__new__(cls)
                cls._instance.logger = cls._setup_logger(log_file)
            return cls._instance
    
    @staticmethod
    def _setup_logger(log_file: str):
        logger = logging.getLogger("zomato_backend")
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger

class ZomatoError(Exception):
    """Base exception class for Zomato backend"""
    pass

class UserNotFoundError(ZomatoError):
    """Raised when a user is not found"""
    pass

class RestaurantNotFoundError(ZomatoError):
    """Raised when a restaurant is not found"""
    pass

class OrderProcessingError(ZomatoError):
    """Raised when order processing fails"""
    pass

class PaymentFailedError(ZomatoError):
    """Raised when payment processing fails"""
    pass