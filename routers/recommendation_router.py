from fastapi import APIRouter, Depends
from auth.jwt_bearer import JWTBearer
from schemas.recommendation_schema import RecommendationInput

recommendations_router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
    dependencies=[Depends(JWTBearer())]
)

@recommendations_router.post("")
def get_recommendations(data: RecommendationInput):

    score = data.prediction
    stress = data.StressLevel

    recs = []

    if score == "Insomnia":
        recs.append("Evita pantallas 1 hora antes de dormir.")
        recs.append("Realiza respiración profunda antes de acostarte.")

    if score == "Sleep Apnea":
        recs.append("Duerme de lado para reducir bloqueos respiratorios.")
        recs.append("Evita alcohol 3 horas antes de dormir.")

    if stress >= 7:
        recs.append("Practica meditación 5–10 minutos diarios.")

    if not recs:
        recs.append("Tus hábitos se ven equilibrados. ¡Sigue así!")

    return {"recommendations": recs}
