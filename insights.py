# Analytics Module

import threading
from typing import Dict, List
from core.utilities import FileHandler

class AnalyticsEngine:
    def __init__(self):
        self._orders_file = "data/orders.json"
        self._restaurants_file = "data/restaurants.json"
        self._users_file = "data/users.json"
        self._lock = threading.Lock()
    
    def get_sales_analytics(self, time_period: str = "daily") -> Dict:
        with self._lock:
            orders = FileHandler.read_json(self._orders_file)
            
            if time_period == "daily":
                return self._aggregate_by_day(orders)
            elif time_period == "weekly":
                return self._aggregate_by_week(orders)
            elif time_period == "monthly":
                return self._aggregate_by_month(orders)
            else:
                raise ValueError("Invalid time period")
    
    def _aggregate_by_day(self, orders: Dict) -> Dict:
        daily_sales = {}
        for order in orders.values():
            date = order['created_at'][:10]  # Extract YYYY-MM-DD
            total = sum(item['price'] * item['quantity'] for item in order['items'])
            
            if date in daily_sales:
                daily_sales[date] += total
            else:
                daily_sales[date] = total
        
        return {
            'period': 'daily',
            'data': daily_sales
        }
    
    def get_restaurant_performance(self, restaurant_id: str) -> Dict:
        with self._lock:
            orders = FileHandler.read_json(self._orders_file)
            restaurant_orders = [
                order for order in orders.values() 
                if order['restaurant_id'] == restaurant_id
            ]
            
            total_orders = len(restaurant_orders)
            total_revenue = sum(
                sum(item['price'] * item['quantity'] for item in order['items'])
                for order in restaurant_orders
            )
            
            return {
                'restaurant_id': restaurant_id,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'avg_order_value': total_revenue / total_orders if total_orders else 0
            }