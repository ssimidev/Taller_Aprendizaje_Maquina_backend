# Backend – Taller de Aprendizaje de Máquina  
API para predicción, explicación y recomendación de calidad del sueño

---

## Descripción del Proyecto

Este backend implementa una API desarrollada con **FastAPI** que permite predecir la calidad del sueño (1–10), clasificar posibles trastornos (Insomnia y Sleep Apnea), generar explicaciones mediante **SHAP** y entregar recomendaciones personalizadas según los factores más influyentes.  
Es consumido por un frontend desarrollado en React y forma parte de un sistema integral orientado a salud preventiva y apoyo a la toma de decisiones.

El backend cumple con los **requerimientos funcionales y no funcionales**, incorporando autenticación segura, modelos de Machine Learning, pipeline de preprocesamiento, modularidad y arquitectura apta para despliegue en la nube.

---

## ✔ Requerimientos Funcionales

### **RF-01 – Onboarding de Usuario**
Permite registrar y autenticar usuarios utilizando JWT y passwords cifrados con Argon2.

### **RF-02 – Formulario de Entrada**
Recibe datos enviados desde el frontend y los valida mediante Pydantic antes de procesarlos.

### **RF-03 – Procesamiento y Predicción**
El endpoint `/predict` ejecuta:
- Preprocesamiento (ColumnTransformer)
- Modelos ML (Random Forest / XGBoost)
- Obtención de predicciones numéricas y categóricas

### **RF-04 – Dashboard de Resultados**
La API entrega la predicción lista para visualización en el frontend.

### **RF-05 – Explicabilidad (XAI)**
El endpoint `/explain` devuelve valores SHAP de las características utilizadas.

### **RF-06 – Historial y Tendencias**
El sistema permite extenderse para almacenar predicciones por usuario.

---

## ✔ Requerimientos No Funcionales

### **RNF-01 – Usabilidad**

### **RNF-02 – Explicabilidad**
SHAP integrado para interpretar el modelo.

### **RNF-03 – Escalabilidad**
Arquitectura modular apta para AWS Lambda + API Gateway.

### **RNF-04 – Seguridad**
Incluye:
- JWT Bearer
- Argon2 para contraseñas
- CORS configurado
- Validación estricta con Pydantic

### **RNF-05 – Confiabilidad**
Modelos entrenados con validación cruzada y almacenados como artefactos reproducibles.

### **RNF-06 – Monitoreabilidad**
Estructura preparada para Prometheus y logging estructurado.

---

## 📁 Estructura del Proyecto

