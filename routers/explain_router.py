from fastapi import APIRouter
from ml.model_loader import model, explainer, preprocess
import pandas as pd

explain_router = APIRouter(prefix="/explain", tags=["Explain"])

@explain_router.post("/")
def explain_instance(data: dict):
    df = pd.DataFrame([data])
    X = preprocess.transform(df)

    shap_values = explainer.shap_values(X)[0].tolist()
    prediction = model.predict(X)[0]

    return {
        "prediction": prediction,
        "shap_values": shap_values
    }
