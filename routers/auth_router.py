from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import argon2
from pydantic import BaseModel
from database import SessionLocal
from models.user import User
from auth.jwt_handler import sign_jwt

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

class UserAuth(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/register")
def register_user(data: UserAuth, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed = argon2.hash(data.password)
    new_user = User(username=data.username, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario creado correctamente"}

@auth_router.post("/login")
def login_user(data: UserAuth, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not argon2.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {"access_token": sign_jwt(user.id), "token_type": "Bearer"}
