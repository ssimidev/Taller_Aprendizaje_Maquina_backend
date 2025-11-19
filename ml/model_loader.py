import pandas as pd
import numpy as np
import joblib
import shap


model = joblib.load("ml/model_rf.pkl")
preprocess = joblib.load("ml/preprocess.pkl")


explainer = shap.TreeExplainer(model)


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

    row = {col: data.get(col, None) for col in EXPECTED_COLUMNS}
    df = pd.DataFrame([row])


    X = preprocess.transform(df)

    if hasattr(X, "toarray"):
        X = X.toarray()

    X = X.astype(np.float64)

   
    y_pred = model.predict(X)[0]


    shap_values = explainer.shap_values(X)
    shap_values_list = shap_values[0].tolist()

    return {
        "prediction": y_pred,
        "shap_values": shap_values_list
    }
