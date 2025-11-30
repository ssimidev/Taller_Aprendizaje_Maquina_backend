from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, nullable=True)
    password = Column(String)

    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    sleep_goal_hours = Column(Float, default=8.0) 
    preferences = Column(JSON, nullable=True)    
    created_at = Column(String, default=func.now())
    updated_at = Column(String, onupdate=func.now())
    last_login = Column(String, nullable=True)
    login_count = Column(Integer, default=0)
    role = Column(String, default="user")
    is_active = Column(Integer, default=1)
