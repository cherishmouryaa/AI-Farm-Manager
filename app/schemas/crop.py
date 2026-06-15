from pydantic import BaseModel
from typing import List

class CropAnalysisQuery(BaseModel):
    crop_type: str
    symptoms: List[str] | None = None

class CropAnalysisResponse(BaseModel):
    crop_type: str
    health_status: str
    issues: List[str]
    recommendation: str
