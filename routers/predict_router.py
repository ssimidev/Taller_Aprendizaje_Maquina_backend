from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from auth.jwt_bearer import JWTBearer
from ml.model_loader import predict
from database import SessionLocal
from models.prediction import Prediction
from datetime import datetime
import json

from datetime import datetime
import pytz

chile_tz = pytz.timezone("America/Santiago")

timestamp = datetime.now(chile_tz)

predict_router = APIRouter(tags=["Prediction"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@predict_router.post("/predict", dependencies=[Depends(JWTBearer())])
def predict_endpoint(
    data: dict = Body(...),
    user_id=Depends(JWTBearer()),
    db: Session = Depends(get_db)
):

    model_name = data.get("model", "rf")


    result = predict(data, model_name=model_name)

    entry = Prediction(
        user_id=user_id,
        prediction_value=result["prediction"],
        timestamp=datetime.now(pytz.timezone("America/Santiago")),
        features=json.dumps(data),
        shap_values=json.dumps(result["shap_values"])
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return result
