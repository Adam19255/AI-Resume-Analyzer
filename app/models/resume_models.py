from pydantic import BaseModel # Pydantic is used by FastAPI for data validation.
from typing import List, Dict

# JSON schema for the /analyze response
class AnalysisResponse(BaseModel):
    score: float
    missing_keywords: List[str]
    recommendations: List[str]
    metrics: Dict[str, float]
