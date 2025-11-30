import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User
from database import SessionLocal
from passlib.hash import argon2


def create_user(
    username,
    password,
    email=None,
    name=None,
    age=None,
    gender=None,
    avatar_url=None,
    role="user",
    sleep_goal_hours=8.0,
    preferences=None
):
    db = SessionLocal()

    hashed_password = argon2.hash(password)

    user = User(
        username=username,
        password=hashed_password,
        email=email,
        name=name,
        age=age,
        gender=gender,
        avatar_url=avatar_url,
        role=role,
        sleep_goal_hours=sleep_goal_hours,
        preferences=preferences,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print("\n Usuario creado exitosamente:")
    print(f"ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print("Password hash:", user.password)


if __name__ == "__main__":
    create_user(
        username="admin",
        password="admin123",
        email="admin@sleep.com",
        name="Administrador General",
        age=30,
        gender="Male",
        avatar_url="https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        role="admin",
        sleep_goal_hours=8.0,
        preferences=None
    )
