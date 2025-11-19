from fastapi import APIRouter, Depends, Body
from auth.jwt_bearer import JWTBearer
from ml.model_loader import predict

predict_router = APIRouter(tags=["Prediction"])

@predict_router.post("/predict", dependencies=[Depends(JWTBearer())])
def predict_endpoint(data: dict = Body(...)):
    return predict(data)
