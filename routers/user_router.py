from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from models.prediction import Prediction
from models.history import History
from auth.jwt_bearer import JWTBearer
from passlib.hash import argon2
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

users_router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_admin(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado (solo administradores)")
    return user


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    sleep_goal_hours: Optional[float] = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str

class AdminCreateUser(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    role: str = "user"
    is_active: int = 1

class AdminUpdateUser(BaseModel):
    username: Optional[str]
    email: Optional[str]
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    role: Optional[str]
    is_active: Optional[int]


def log_event(db, user_id, event_type, description, metadata=None):
    entry = History(
        user_id=user_id,
        event_type=event_type,
        description=description,
        timestamp=datetime.utcnow().isoformat(),
        metadata=json.dumps(metadata) if metadata else None
    )
    db.add(entry)
    db.commit()


@users_router.get("/me")
def get_me(user_id=Depends(JWTBearer()), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "age": user.age,
        "gender": user.gender,
        "sleep_goal_hours": user.sleep_goal_hours,
        "role": user.role,
        "is_active": user.is_active,
    }


@users_router.put("/update")
def update_user(data: UpdateUser, user_id=Depends(JWTBearer()), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    log_event(db, user_id, "profile_update", "Actualizó su perfil")

    return {"message": "Perfil actualizado"}


@users_router.put("/change-password")
def change_password(data: ChangePassword, user_id=Depends(JWTBearer()), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not argon2.verify(data.old_password, user.password):
        raise HTTPException(400, "Contraseña actual incorrecta")

    user.password = argon2.hash(data.new_password)
    db.commit()

    log_event(db, user_id, "password_change", "Cambió su contraseña")

    return {"message": "Contraseña actualizada"}


@users_router.get("/history")
def get_prediction_history(user_id=Depends(JWTBearer()), db: Session = Depends(get_db)):
    predictions = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.timestamp.desc())
        .all()
    )

    return [
        {
            "id": p.id,
            "prediction_value": p.prediction_value,
            "timestamp": p.timestamp,
            "features": p.features,
            "shap_values": p.shap_values,
        }
        for p in predictions
    ]


@users_router.delete("/history")
def clear_prediction_history(user_id=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db.query(Prediction).filter(Prediction.user_id == user_id).delete()
    db.commit()

    log_event(db, user_id, "clear_prediction_history", "Eliminó su historial")

    return {"message": "Historial eliminado"}


@users_router.delete("/delete-account")
def delete_account(user_id=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db.query(Prediction).filter(Prediction.user_id == user_id).delete()
    db.query(User).filter(User.id == user_id).delete()
    db.commit()

    return {"message": "Cuenta eliminada"}


@users_router.get("/history-extended")
def get_detailed_history(user_id=Depends(JWTBearer()), db: Session = Depends(get_db)):
    history = (
        db.query(History)
        .filter(History.user_id == user_id)
        .order_by(History.timestamp.desc())
        .all()
    )

    return [
        {
            "id": h.id,
            "event_type": h.event_type,
            "description": h.description,
            "timestamp": h.timestamp,
            "metadata": json.loads(h.metadata) if h.metadata else None
        }
        for h in history
    ]

@users_router.get("")
def admin_get_all_users(admin_id=Depends(JWTBearer()), db: Session = Depends(get_db)):
    require_admin(admin_id, db)

    users = db.query(User).all()
    return users


@users_router.post("")
def admin_create_user(
    data: AdminCreateUser,
    admin_id=Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    require_admin(admin_id, db)

    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(400, "El nombre de usuario ya existe")

    hashed = argon2.hash(data.password)

    user = User(
        username=data.username,
        email=data.email,
        password=hashed,
        name=data.name,
        age=data.age,
        gender=data.gender,
        role=data.role,
        is_active=data.is_active
    )

    db.add(user)
    db.commit()

    return {"message": "Usuario creado con éxito"}


@users_router.put("/{user_id}")
def admin_update_user(
    user_id: int,
    data: AdminUpdateUser,
    admin_id = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return {"message": "Usuario actualizado correctamente"}

@users_router.delete("/{user_id}")
def admin_delete_user(user_id: int, admin_id=Depends(JWTBearer()), db: Session = Depends(get_db)):
    require_admin(admin_id, db)

    db.query(Prediction).filter(Prediction.user_id == user_id).delete()
    db.query(User).filter(User.id == user_id).delete()
    db.commit()

    return {"message": "Usuario eliminado correctamente"}
