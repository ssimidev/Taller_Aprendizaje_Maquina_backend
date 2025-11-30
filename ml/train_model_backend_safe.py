import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

print("\nCargando dataset...")
df = pd.read_csv("Sleep_dataset.csv")

print("\n==== Columnas detectadas en el CSV ====")
for c in df.columns:
    print(repr(c))
print("\n Normalizando nombres de columnas...")

df.columns = (
    df.columns
    .str.strip()
    .str.replace("\u00A0", "", regex=False)   
    .str.replace("\t", "", regex=False)     
    .str.replace("  ", " ", regex=False)    
)

# Buscar variaciones de Sleep Disorder
for col in df.columns:
    key = col.replace(" ", "").lower()
    if key in ["sleepdisorder", "sleep-disorder", "sleep_disorder"]:
        if col != "Sleep Disorder":
            print(f"➡ Renombrando '{col}' → 'Sleep Disorder'")
        df = df.rename(columns={col: "Sleep Disorder"})
        break

print("\nColumnas finales:")
print(df.columns.tolist())

print("\n Valores faltantes encontrados por columna:")
print(df.isna().sum())

print("\n Corrigiendo NaN...")
df["Sleep Disorder"] = df["Sleep Disorder"].fillna("None")

TARGET = "Quality of Sleep"

X = df.drop(columns=[TARGET])
y = df[TARGET]

print(X.columns.tolist())

categorical_cols = [
    "Gender",
    "Occupation",
    "BMI Category",
    "Blood Pressure",
    "Sleep Disorder",
]

numeric_cols = [
    c for c in X.columns if c not in categorical_cols
]

print("\n Columnas categóricas:", categorical_cols)
print(" Columnas numéricas:", numeric_cols)

preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numeric_cols),
    ]
)

print("\n⚙ Entrenando modelo...")

pipeline = Pipeline(steps=[
    ("preprocess", preprocess),
    ("model", RandomForestRegressor(n_estimators=200, random_state=42))
])

pipeline.fit(X, y)

print("\n Modelo entrenado correctamente.")

joblib.dump(pipeline.named_steps["preprocess"], "preprocess.pkl")
joblib.dump(pipeline.named_steps["model"], "model_rf.pkl")

print("\n Archivos guardados:")
print(" - preprocess.pkl")
print(" - model_rf.pkl")

print("\n ENTRENAMIENTO COMPLETADO SIN ERRORES\n")
