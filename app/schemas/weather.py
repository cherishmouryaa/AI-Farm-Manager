from pydantic import BaseModel

class WeatherQuery(BaseModel):
    location: str

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    condition: str
    recommendation: str
