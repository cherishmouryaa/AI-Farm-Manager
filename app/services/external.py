import httpx
from app.core.config import settings

class ExternalWeatherService:
    """
    Service to interact with external weather APIs (e.g. OpenWeatherMap).
    """
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"

    async def get_current_weather(self, lat: float, lon: float) -> dict:
        # Skeleton call (requires valid API key and active connection)
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(f"{self.base_url}/weather", params={"lat": lat, "lon": lon, "appid": self.api_key})
        #     return response.json()
        return {"status": "mocked", "temperature": 25.0, "humidity": 60}
