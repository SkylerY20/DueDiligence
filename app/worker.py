from celery import Celery
import os

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(__name__, broker=redis_url, backend=redis_url)

@celery_app.task
def analyze_task(data):
    # Simulate analysis
    return {"analysis": "completed", "input": data}
