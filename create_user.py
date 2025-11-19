import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User
from database import SessionLocal
from passlib.hash import argon2


def create_user(username, password):
    db = SessionLocal()

    hashed_password = argon2.hash(password)

    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    print("\nUsuario creado exitosamente:")
    print("Username:", user.username)
    print("Password hash:", user.password)


if __name__ == "__main__":
    create_user("Prueba", "Prueba")
