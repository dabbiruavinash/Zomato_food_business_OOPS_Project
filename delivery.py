import threading
import random
from typing import Dict, List
from core.utilities import FileHandler
from core.exceptions import OrderProcessingError

class DeliveryManager:
    def __init__(self):
        self._file_path = "data/deliveries.json"
        self._deliveries = FileHandler.read_json(self._file_path)
        self._lock = threading.Lock()
        self._delivery_threads = {}
    
    def assign_delivery(self, order_id: str) -> str:
        delivery_id = f"delivery_{len(self._deliveries) + 1}"
        delivery_data = {
            'id': delivery_id,
            'order_id': order_id,
            'status': 'assigned',
            'delivery_person': self._get_available_delivery_person(),
            'assigned_at': datetime.now().isoformat()
        }
        
        with self._lock:
            self._deliveries[delivery_id] = delivery_data
            FileHandler.write_json(self._file_path, self._deliveries)
        
        # Start delivery tracking in background
        delivery_thread = threading.Thread(
            target=self._track_delivery,
            args=(delivery_id,)
        )
        delivery_thread.start()
        self._delivery_threads[delivery_id] = delivery_thread
        
        return delivery_id
    
    def _get_available_delivery_person(self) -> str:
        # Simplified - in real app would query available delivery people
        return f"delivery_person_{random.randint(1, 100)}"
    
    def _track_delivery(self, delivery_id: str):
        try:
            # Simulate delivery stages
            time.sleep(2)
            self._update_delivery_status(delivery_id, "picked_up")
            
            time.sleep(5)
            self._update_delivery_status(delivery_id, "in_transit")
            
            time.sleep(3)
            self._update_delivery_status(delivery_id, "delivered")
            
        except Exception as e:
            self._update_delivery_status(delivery_id, "failed")
            raise OrderProcessingError(f"Delivery failed: {str(e)}")
    
    def _update_delivery_status(self, delivery_id: str, status: str):
        with self._lock:
            if delivery_id not in self._deliveries:
                raise OrderProcessingError(f"Delivery {delivery_id} not found")
            
            self._deliveries[delivery_id]['status'] = status
            self._deliveries[delivery_id]['updated_at'] = datetime.now().isoformat()
            FileHandler.write_json(self._file_path, self._deliveries)