from fastapi import APIRouter, HTTPException
from app.schemas.weather import WeatherQuery, WeatherResponse

router = APIRouter()

@router.post("/query", response_model=WeatherResponse)
async def query_weather(query: WeatherQuery):
    """
    Query weather conditions and get recommendations from the Weather Agent.
    """
    # Placeholder response
    return WeatherResponse(
        location=query.location,
        temperature=25.0,
        condition="Sunny",
        recommendation="Ideal conditions for crop spraying. No rain forecast for the next 24 hours."
    )
