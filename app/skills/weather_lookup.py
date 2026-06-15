from typing import Any, Dict
from app.skills.base import BaseSkill

class WeatherLookupSkill(BaseSkill):
    """
    Skill for retrieving mock weather details or forecasts for a location.
    """
    def __init__(self):
        super().__init__(
            name="Weather Lookup",
            description="Fetches weather forecasts, humidity, rain probability, and temperature."
        )
        # Simple offline mock database for locations
        self.mock_db = {
            "california": {
                "temperature": 28.5,
                "humidity": 35,
                "rain_probability": 0,
                "forecast": "Sunny and dry, mild heatwave expected over next 3 days."
            },
            "iowa": {
                "temperature": 22.0,
                "humidity": 75,
                "rain_probability": 80,
                "forecast": "Heavy showers expected tomorrow, high humidity."
            },
            "texas": {
                "temperature": 32.0,
                "humidity": 50,
                "rain_probability": 20,
                "forecast": "Partly cloudy, warm, light winds."
            }
        }

    async def run(self, location: str, **kwargs) -> Dict[str, Any]:
        loc_key = location.lower().strip()
        # Default mock response if location not in list
        return self.mock_db.get(loc_key, {
            "temperature": 24.0,
            "humidity": 55,
            "rain_probability": 10,
            "forecast": f"Moderate weather in {location}. Light breeze, no major storm systems."
        })
