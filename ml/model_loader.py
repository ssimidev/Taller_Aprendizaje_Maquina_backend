import pandas as pd
import numpy as np
import joblib

model = joblib.load("ml/model_rf.pkl")
preprocess = joblib.load("ml/preprocess.pkl")
explainer = joblib.load("ml/shap_explainer.pkl")

EXPECTED_COLUMNS = [
    "Person ID",
    "Gender",
    "Age",
    "Occupation",
    "Sleep Duration",
    "Physical Activity Level",
    "Stress Level",
    "BMI Category",
    "Blood Pressure",
    "Heart Rate",
    "Daily Steps",
    "Sleep Disorder"
]

def predict(data: dict):
    # Asegurar orden y columnas faltantes
    row = {col: data.get(col, None) for col in EXPECTED_COLUMNS}
    df = pd.DataFrame([row])

    # Transformación del pipeline
    X = preprocess.transform(df)


    if hasattr(X, "toarray"):
        X = X.toarray()

    # Convertir SIEMPRE a float64
    X = X.astype(np.float64)

    # Predicción
    y_pred = model.predict(X)[0]

    # SHAP seguro
    shap_vals = explainer.shap_values(X)[0].tolist()

    return {
        "prediction": y_pred,
        "shap_values": shap_vals
    }
