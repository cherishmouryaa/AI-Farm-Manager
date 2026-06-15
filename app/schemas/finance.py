from pydantic import BaseModel
from typing import List

class FinanceQuery(BaseModel):
    estimated_costs: float
    expected_yield: float
    price_per_unit: float

class FinanceResponse(BaseModel):
    total_costs: float
    projected_revenue: float
    expected_roi: float
    recommendations: List[str]
