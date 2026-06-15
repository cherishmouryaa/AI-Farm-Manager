from typing import Any, Dict
from app.agents.base import BaseAgent
from app.skills.weather_lookup import WeatherLookupSkill

class WeatherAgent(BaseAgent):
    """
    Agent responsible for monitoring and analyzing weather conditions.
    """
    def __init__(self, **kwargs):
        super().__init__(
            name="Weather Agent",
            role="Provides localized weather analysis and forecasts, recommending farming adjustments.",
            **kwargs
        )

    async def run(self, input_text: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        # Extract location from input/context
        location = context.get("location", input_text) if context else input_text
        
        # Find WeatherLookupSkill
        weather_tool = next((s for s in self.skills if isinstance(s, WeatherLookupSkill)), None)
        if not weather_tool:
            weather_tool = WeatherLookupSkill()  # Fallback instantiating
            
        weather_data = await weather_tool.run(location=location)
        
        # Analyze weather data
        analysis = f"Forecast for {location} is: {weather_data['forecast']}. Temp: {weather_data['temperature']}C, Humidity: {weather_data['humidity']}%."
        
        # Operational restriction logic based on weather
        action_restriction = "none"
        if weather_data["rain_probability"] > 60:
            action_restriction = "delay spraying and harvesting"
        elif weather_data["temperature"] > 35:
            action_restriction = "restrict heavy labor to morning, increase irrigation"

        result = {
            "agent": self.name,
            "status": "success",
            "weather_data": weather_data,
            "analysis": analysis,
            "action_restriction": action_restriction
        }
        
        # Write to memory if available
        if self.memory:
            self.memory.add({"sender": self.name, "topic": "weather_report", "data": result})
            
        return result
