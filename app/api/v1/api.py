from fastapi import APIRouter

from app.api.v1.endpoints import weather, crop, planner, finance

api_router = APIRouter()

api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(crop.router, prefix="/crop", tags=["crop"])
api_router.include_router(planner.router, prefix="/planner", tags=["planner"])
api_router.include_router(finance.router, prefix="/finance", tags=["finance"])
