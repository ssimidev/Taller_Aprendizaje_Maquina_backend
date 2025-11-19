from pydantic import BaseModel
from typing import Optional

class RecommendationInput(BaseModel):
    prediction: str
    StressLevel: Optional[int] = 0
