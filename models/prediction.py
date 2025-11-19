from sqlalchemy import Column, Integer, Float, String, ForeignKey
from database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prediction_value = Column(Float)
    shap_values = Column(String)
    features = Column(String)
    timestamp = Column(String)
