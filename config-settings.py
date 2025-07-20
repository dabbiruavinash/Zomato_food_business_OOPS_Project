import os
import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
      _instance = None

      def __new__(cls):
             if cls._instance is None:
                cls._instance = super(ConfigManager, cls).__init__(cls)
                cls._instance._load_config()
             return cls._instance

      def _load_config(self):
            config_path = Path(__file__).parent  / "config.json"
            with open(config_path) as f:
                   self._config = json.load(f)

            # Load environment variable
            self._config["database"] = {
                 "host" : os.getenv("DB_HOST"),
                 "port" : os.getenv("DB_PORT"),
                 "user" : os.getenv("DB_USER"),
                 "password" : os.getenv("DB_PASSWORD")
}

           def get(self, key:str, default: Any = None) -> Any:
                  return self._config.get(key, default)

class OrderStatus:
         PENDING = "pending"
         CONFIRMED = "confirmed"
         PREPARING = "preparing"
         OUT_FOR_DELIVERY = "out_for_delivery"
         DELIVERED = "delivered"
         CANCELLED = "cancelled"

class PaymentStatus:
         PENDING = "pending"
         COMPLETED = "completed"
         FAILED = "failed"
         REFUNDED = "refunded"