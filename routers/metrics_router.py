from fastapi import APIRouter
import time
import psutil

metrics_router = APIRouter(prefix="/metrics", tags=["Monitoring"])

@metrics_router.get("")
def get_metrics():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    return {
        "cpu_usage": cpu,
        "memory_usage": mem,
        "timestamp": time.time()
    }
