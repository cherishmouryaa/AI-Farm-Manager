from pydantic import BaseModel
from typing import List, Dict, Any

class PlanQuery(BaseModel):
    duration_days: int = 7
    preferences: Dict[str, Any] | None = None

class PlanResponse(BaseModel):
    tasks: List[Dict[str, Any]]
    summary: str
