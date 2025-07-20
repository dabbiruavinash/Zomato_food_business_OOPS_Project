import threading
import uuid
from queue import Queue
from threading import Thread
from typing import Dict, List
from core.utilities import FileHandler
from core.exceptions import OrderProcessingError

class OrderProcessor:
    def __init__(self):
        self._file_path = "data/orders.json"
        self._orders = FileHandler.read_json(self._file_path)
        self._order_queue = Queue()
        self._lock = threading.Lock()
        self._processing_thread = Thread(target=self._process_orders)
        self._processing_thread.daemon = True
        self._processing_thread.start()
    
    def create_order(self, user_id: str, restaurant_id: str, items: List[Dict]) -> str:
        order_id = f"order_{uuid.uuid4().hex[:8]}"
        order_data = {
            'id': order_id,
            'user_id': user_id,
            'restaurant_id': restaurant_id,
            'items': items,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        with self._lock:
            self._orders[order_id] = order_data
            FileHandler.write_json(self._file_path, self._orders)
        
        self._order_queue.put(order_id)
        return order_id
    
    def _process_orders(self):
        while True:
            order_id = self._order_queue.get()
            try:
                self._process_single_order(order_id)
            except Exception as e:
                print(f"Error processing order {order_id}: {str(e)}")
            finally:
                self._order_queue.task_done()
    
    def _process_single_order(self, order_id: str):
        with self._lock:
            if order_id not in self._orders:
                raise OrderProcessingError(f"Order {order_id} not found")
            
            order = self._orders[order_id]
            order['status'] = 'processing'
            order['updated_at'] = datetime.now().isoformat()
            FileHandler.write_json(self._file_path, self._orders)
        
        # Simulate order processing
        time.sleep(2)
        
        with self._lock:
            order['status'] = 'completed'
            order['updated_at'] = datetime.now().isoformat()
            FileHandler.write_json(self._file_path, self._orders)