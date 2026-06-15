from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.core.config import settings
from app.api.v1.api import api_router

from app.memory.short_term import ShortTermMemory
from app.memory.long_term import LongTermMemory

from app.skills.weather_lookup import WeatherLookupSkill
from app.skills.crop_analysis import CropAnalysisSkill
from app.skills.finance_calc import FinanceCalcSkill

from app.agents.weather import WeatherAgent
from app.agents.crop import CropAgent
from app.agents.finance import FinanceAgent
from app.agents.planner import PlannerAgent

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve frontend files
app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

# Long-term memory
long_term_mem = LongTermMemory()


class FarmPlanRequest(BaseModel):
    location: str
    crop: str
    farm_size: float


# Homepage = Frontend
@app.get("/")
async def home():
    return FileResponse("frontend/index.html")


# Farm Plan API
@app.post("/farm-plan")
async def generate_farm_plan(payload: FarmPlanRequest):

    # Session memory
    short_term_mem = ShortTermMemory()

    # Skills
    weather_skill = WeatherLookupSkill()
    crop_skill = CropAnalysisSkill()
    finance_skill = FinanceCalcSkill()

    # Agents
    weather_agent = WeatherAgent(
        memory=short_term_mem,
        skills=[weather_skill]
    )

    crop_agent = CropAgent(
        memory=short_term_mem,
        skills=[crop_skill]
    )

    finance_agent = FinanceAgent(
        memory=short_term_mem,
        skills=[finance_skill]
    )

    planner_agent = PlannerAgent(
        memory=short_term_mem,
        long_term_memory=long_term_mem
    )

    # Agent workflow
    await weather_agent.run(
        input_text=payload.location
    )

    await crop_agent.run(
        input_text="",
        context={
            "crop_type": payload.crop,
            "farm_size_acres": payload.farm_size
        }
    )

    await finance_agent.run(
        input_text="",
        context={
            "crop_type": payload.crop,
            "farm_size_acres": payload.farm_size
        }
    )

    final_plan = await planner_agent.run(
        input_text="Generate plan"
    )

    return final_plan