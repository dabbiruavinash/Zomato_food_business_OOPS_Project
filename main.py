from fastapi import FastAPI
from modules.api_gateway.api import app
import uvicorn
import threading
from modules.cache_service.cache import CacheManager
from modules.analytics.insights import AnalyticsEngine

def initialize_background_services():
    # Initialize cache
    CacheManager()
    
    # Start analytics periodic updates
    analytics = AnalyticsEngine()
    threading.Thread(
        target=analytics.run_periodic_updates,
        daemon=True
    ).start()

if __name__ == "__main__":
    initialize_background_services()
    uvicorn.run(app, host="0.0.0.0", port=8000)