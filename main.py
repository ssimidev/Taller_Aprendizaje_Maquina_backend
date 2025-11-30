from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine

# Routers existentes
from routers.auth_router import auth_router
from routers.predict_router import predict_router
from routers.explain_router import explain_router
from routers.metrics_router import metrics_router
from routers.user_router import users_router

# Nuevo router
from routers.recommendation_router import recommendations_router


app = FastAPI(
    title="Sleep Quality API",
    version="1.0.0",
    description="Backend para predicción y explicabilidad de calidad del sueño"
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(predict_router)
app.include_router(explain_router)
app.include_router(recommendations_router)   
app.include_router(metrics_router)
app.include_router(users_router)

# =====================================================
# ROOT
# =====================================================
@app.get("/")
def root():
    return {"msg": "API funcionando correctamente"}
