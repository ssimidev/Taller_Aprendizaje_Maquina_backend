from fastapi import APIRouter

health_router = APIRouter(prefix="/health", tags=["Health"])

@health_router.get("")
def health():
    return {"status": "ok"}
