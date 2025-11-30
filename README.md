# Backend – Sistema de Predicción de Calidad del Sueño

Este backend está desarrollado con **FastAPI** y permite:

- Recibir datos desde un formulario del usuario  
- Predecir la calidad del sueño usando modelos de Machine Learning  
- Generar explicaciones SHAP sobre qué influyó en la predicción  
- Entregar recomendaciones personalizadas  
- Conectarse con el frontend para mostrar resultados en un dashboard  

Es parte del proyecto **Taller de Aprendizaje de Máquina**.

---

## Requisitos Previos

- Python 3.10+
- pip instalado
- Dataset `Sleep_dataset.csv`

---

## Instalación Rápida

### 1️Clonar el repositorio

git clone <url-del-repo>
cd Taller_Aprendizaje_Maquina_backend

### Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows

## Instalar dependencias
pip install -r requirements.txt


## Colocar el dataset en la carpeta /ml
/ml/Sleep_dataset.csv

## Ejecutar el script de entrenamiento
python ml/train_model_backend_safe.py


## Crear Usuario Administrador
python create_user.py

## Ejecutar el Servidor
uvicorn main:app --reload


## Estructura del Proyecto
/ml               → Modelos, SHAP, preprocesador y scripts de entrenamiento
/auth             → Login, registro y JWT
/routers          → Endpoints de la API
/schemas          → Validación con Pydantic
/models           → ORM con SQLAlchemy
main.py           → Configuración principal del backend
