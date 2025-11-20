from fastapi import FastAPI
from celery.result import AsyncResult
from .worker import celery_app, analyze_task

app = FastAPI()

@app.post("/analyze")
async def analyze(data: dict):
    task = analyze_task.delay(data)
    return {"task_id": task.id}

@app.get("/analyze/{task_id}")
async def get_analysis(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.ready():
        return {"status": "completed", "result": task_result.result}
    return {"status": "processing"}
