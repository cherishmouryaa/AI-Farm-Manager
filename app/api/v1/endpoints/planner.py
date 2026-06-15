from fastapi import APIRouter, HTTPException
from app.schemas.planner import PlanQuery, PlanResponse

router = APIRouter()

@router.post("/plan", response_model=PlanResponse)
async def generate_plan(query: PlanQuery):
    """
    Generate seasonal or weekly farming tasks and plans using the Planner Agent.
    """
    # Placeholder response
    return PlanResponse(
        tasks=[
            {"id": 1, "task": "Check soil moisture levels in Zone A", "priority": "High"},
            {"id": 2, "task": "Apply organic fertilizer to tomatoes", "priority": "Medium"}
        ],
        summary="Weekly plan focused on moisture monitoring and nutritional balance."
    )
