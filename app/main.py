from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)
# Include main router
app.include_router(api_router, prefix=settings.API_V1_STR)

from pydantic import BaseModel
from app.memory.short_term import ShortTermMemory
from app.memory.long_term import LongTermMemory
from app.skills.weather_lookup import WeatherLookupSkill
from app.skills.crop_analysis import CropAnalysisSkill
from app.skills.finance_calc import FinanceCalcSkill
from app.agents.weather import WeatherAgent
from app.agents.crop import CropAgent
from app.agents.finance import FinanceAgent
from app.agents.planner import PlannerAgent

class FarmPlanRequest(BaseModel):
    location: str
    crop: str
    farm_size: float

# Initialize Long-Term Memory once at startup
long_term_mem = LongTermMemory()

@app.get("/")
async def root():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME} API",
        "docs_url": "/docs"
    }

@app.post("/farm-plan")
async def generate_farm_plan(payload: FarmPlanRequest):
    # 1. Initialize Short-Term Memory for this session
    short_term_mem = ShortTermMemory()
    
    # 2. Initialize Skills
    weather_skill = WeatherLookupSkill()
    crop_skill = CropAnalysisSkill()
    finance_skill = FinanceCalcSkill()
    
    # 3. Initialize Agents
    weather_agent = WeatherAgent(memory=short_term_mem, skills=[weather_skill])
    crop_agent = CropAgent(memory=short_term_mem, skills=[crop_skill])
    finance_agent = FinanceAgent(memory=short_term_mem, skills=[finance_skill])
    planner_agent = PlannerAgent(memory=short_term_mem, long_term_memory=long_term_mem)
    
    # 4. Multi-agent execution sequence
    await weather_agent.run(input_text=payload.location)
    await crop_agent.run(
        input_text="", 
        context={"crop_type": payload.crop, "farm_size_acres": payload.farm_size}
    )
    await finance_agent.run(
        input_text="",
        context={"crop_type": payload.crop, "farm_size_acres": payload.farm_size}
    )
    plan_res = await planner_agent.run(input_text="Generate plan")
    
    return plan_res
