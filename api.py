from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import json
import threading

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared resources
user_manager = None
restaurant_manager = None
order_processor = None
notification_service = None
analytics_engine = None
recommendation_engine = None

def initialize_services():
    global user_manager, restaurant_manager, order_processor, notification_service, analytics_engine, recommendation_engine
    
    from modules.user_management.user import UserManager
    from modules.restaurant_management.restaurant import RestaurantManager
    from modules.order_processing.order import OrderProcessor
    from modules.notification_service.notifier import NotificationService
    from modules.analytics.insights import AnalyticsEngine
    from modules.recommendation_engine.recommender import RecommendationEngine
    
    user_manager = UserManager()
    restaurant_manager = RestaurantManager()
    order_processor = OrderProcessor()
    notification_service = NotificationService()
    analytics_engine = AnalyticsEngine()
    recommendation_engine = RecommendationEngine()

@app.on_event("startup")
async def startup_event():
    initialize_services()

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        return user_manager.get_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/orders")
async def create_order(order_data: Dict):
    try:
        order_id = order_processor.create_order(
            order_data['user_id'],
            order_data['restaurant_id'],
            order_data['items']
        )
        
        # Send notification
        notification_service.send_order_confirmation(
            order_data['user_id'],
            order_id
        )
        
        return {"order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/restaurants/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    try:
        return recommendation_engine.get_personalized_recommendations(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/analytics/sales")
async def get_sales_analytics(time_period: str = "daily"):
    try:
        return analytics_engine.get_sales_analytics(time_period)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))