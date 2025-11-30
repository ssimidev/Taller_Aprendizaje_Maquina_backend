from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    event_type = Column(String, nullable=False)     # Ej: "prediction", "change_password"
    description = Column(Text, nullable=False)      # Texto visible
    details = Column(Text, nullable=True)           # JSON como string (antes metadata)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
