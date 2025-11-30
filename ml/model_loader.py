import os
import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.pipeline import Pipeline

BASE_DIR = os.path.dirname(__file__)


PREPROCESS_PATH = os.path.join(BASE_DIR, "preprocess.pkl")
MODEL_RF_PATH = os.path.join(BASE_DIR, "model_rf.pkl")
MODEL_XGB_PATH = os.path.join(BASE_DIR, "model_xgb.pkl")


preprocess = joblib.load(PREPROCESS_PATH)

rf_raw = joblib.load(MODEL_RF_PATH)
xgb_raw = joblib.load(MODEL_XGB_PATH)


def extract_model(obj):
    if isinstance(obj, Pipeline):
        for key in obj.named_steps:
       
            if key != "preprocess":
                return obj.named_steps[key]
        raise ValueError("No encuentro el modelo dentro del pipeline.")
    return obj


rf_model = extract_model(rf_raw)
xgb_model = extract_model(xgb_raw)


expl_rf = shap.TreeExplainer(rf_model)
expl_xgb = shap.TreeExplainer(xgb_model)


EXPECTED_COLUMNS = [
    "Person ID", "Gender", "Age", "Occupation", "Sleep Duration",
    "Physical Activity Level", "Stress Level", "BMI Category",
    "Blood Pressure", "Heart Rate", "Daily Steps", "Sleep Disorder"
]


def predict(data: dict, model_name="rf"):

    row = {col: data.get(col, None) for col in EXPECTED_COLUMNS}
    df = pd.DataFrame([row])


    X = preprocess.transform(df)
    if hasattr(X, "toarray"):
        X = X.toarray()


    if model_name == "xgb":
        model = xgb_model
        explainer = expl_xgb
    else:
        model = rf_model
        explainer = expl_rf


    y_pred = model.predict(X)[0]


    shap_values = explainer.shap_values(X)
    try:
        shap_list = shap_values.tolist()[0]
    except:
        shap_list = shap_values[0].tolist()

    return {
        "prediction": float(y_pred),
        "model_used": model_name,
        "shap_values": shap_list
    }
