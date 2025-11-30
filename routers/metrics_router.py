# routers/metrics_router.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from models.prediction import Prediction
import json
import random

metrics_router = APIRouter(prefix="/metrics", tags=["Metrics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0


@metrics_router.get("/stats")
def get_sleep_stats(user_id: int, db: Session = Depends(get_db)):
 
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


    last_prediction = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.timestamp.desc())
        .first()
    )


    if not last_prediction:
        return {
            "sleep_score": 0,
            "sleep_score_change": 0,
            "duration": "0h 0m",
            "duration_change": 0,
            "efficiency": "0%",
            "efficiency_change": 0,
            "time_in_bed": "0h 0m",
            "time_in_bed_change": 0,
            "trend": [0, 0, 0, 0, 0, 0, 0]
        }

   
    try:
        features = json.loads(last_prediction.features)
    except:
        features = {}


    sleep_duration = safe_float(features.get("Sleep Duration", 0))
    physical_activity = safe_float(features.get("Physical Activity Level", 0))
    stress_level = safe_float(features.get("Stress Level", 0))

    
    hours = int(sleep_duration)
    minutes = int((sleep_duration - hours) * 60)

    sleep_score = max(0, min(100, int(
        (sleep_duration * 10)
        + (physical_activity * 0.2)
        - (stress_level * 3)
        + random.randint(-5, 5)
    )))

    # Generar tendencia limpia
    trend = [
        max(0, min(100, sleep_score + random.randint(-10, 10)))
        for _ in range(7)
    ]


    return {
        "sleep_score": sleep_score,
        "sleep_score_change": random.randint(-5, 5),

        "duration": f"{hours}h {minutes}m",
        "duration_change": random.randint(-5, 5),

        "efficiency": f"{max(70, min(99, 100 - stress_level))}%",
        "efficiency_change": random.randint(-5, 5),

        "time_in_bed": f"{hours + 1}h {minutes}m",
        "time_in_bed_change": random.randint(-5, 5),

        "trend": trend
    }
