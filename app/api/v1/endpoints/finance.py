from fastapi import APIRouter, HTTPException
from app.schemas.finance import FinanceQuery, FinanceResponse

router = APIRouter()

@router.post("/budget", response_model=FinanceResponse)
async def analyze_budget(query: FinanceQuery):
    """
    Evaluate crop ROI, calculate costs, and analyze budgets using the Finance Agent.
    """
    # Placeholder response
    return FinanceResponse(
        total_costs=query.estimated_costs,
        projected_revenue=query.estimated_costs * 1.5,
        expected_roi=50.0,
        recommendations=["Invest in automated irrigation to reduce labor cost in the long run."]
    )
