from fastapi import APIRouter, Depends
from auth.jwt_bearer import JWTBearer
from ml.model_loader import (
    rf_model,
    xgb_model,
    expl_rf,
    expl_xgb,
    preprocess,
    EXPECTED_COLUMNS
)
import numpy as np
import pandas as pd

explain_router = APIRouter(
    prefix="/explain",
    tags=["Explainability"],
    dependencies=[Depends(JWTBearer())]
)

@explain_router.post("/{model_name}")
def explain_instance(model_name: str, data: dict):

    # validar modelo
    if model_name not in ["rf", "xgb"]:
        return {"error": "Modelo inválido. Use 'rf' o 'xgb'."}

    # Elige modelo y explainer
    model = rf_model if model_name == "rf" else xgb_model
    explainer = expl_rf if model_name == "rf" else expl_xgb

    # Alinear columnas
    row = {col: data.get(col, None) for col in EXPECTED_COLUMNS}
    df = pd.DataFrame([row])

    # Preprocesar
    X = preprocess.transform(df)
    if hasattr(X, "toarray"):
        X = X.toarray()

    # Obtener SHAP values
    shap_values = explainer.shap_values(X)
    shap_list = shap_values[0].tolist()

    # Obtener predicción
    pred = model.predict(X)[0]

    return {
        "model": model_name,
        "prediction": str(pred),
        "shap_values": shap_list,
        "features": row
    }
