import pandas as pd
import joblib
import shap
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# ======================
# CARGAR DATASET ORIGINAL
# ======================
df = pd.read_csv("Sleep_dataset.csv")   # <-- asegúrate que este archivo esté en backend/

# ======================
# DEFINIR X E Y
# ======================
y = df["Quality of Sleep"]
X = df.drop(columns=["Quality of Sleep"])

# ======================
# COLUMNAS
# ======================
num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

print("Columnas numéricas:", num_cols)
print("Columnas categóricas:", cat_cols)

# ======================
# PREPROCESSOR
# ======================
preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
    ]
)

# ======================
# MODELO
# ======================
model_rf = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1,
)

# ======================
# PIPELINE COMPLETO
# ======================
pipe = Pipeline([
    ("pre", preprocess),
    ("model", model_rf),
])

# ======================
# ENTRENAR
# ======================
print("Entrenando modelo...")
pipe.fit(X, y)
print("Entrenamiento completado.")

# ======================
# EXTRAER OBJETOS DEL PIPELINE
# ======================
preprocessor_fitted = pipe.named_steps["pre"]
model_fitted = pipe.named_steps["model"]

# ======================
# SHAP EXPLAINER
# ======================
print("Creando SHAP explainer...")
explainer = shap.TreeExplainer(model_fitted)

# ======================
# GUARDAR MODELOS
# ======================
joblib.dump(preprocessor_fitted, "ml/preprocess.pkl")
joblib.dump(model_fitted, "ml/model_rf.pkl")
joblib.dump(explainer, "ml/shap_explainer.pkl")

print("Modelos guardados correctamente en /ml/")
