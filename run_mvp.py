import asyncio
import json
from app.memory.short_term import ShortTermMemory
from app.memory.long_term import LongTermMemory

from app.skills.weather_lookup import WeatherLookupSkill
from app.skills.crop_analysis import CropAnalysisSkill
from app.skills.finance_calc import FinanceCalcSkill

from app.agents.weather import WeatherAgent
from app.agents.crop import CropAgent
from app.agents.finance import FinanceAgent
from app.agents.planner import PlannerAgent

async def run_scenario(scenario_id: int, location: str, crop_type: str, farm_size_acres: float, long_term_mem: LongTermMemory):
    print(f"\n==========================================")
    print(f" RUNNING SCENARIO {scenario_id}: {crop_type.upper()} IN {location.upper()} ({farm_size_acres} ACRES)")
    print(f"==========================================")
    
    # 1. Initialize Short-Term Memory for this session
    short_term_mem = ShortTermMemory()
    
    # 2. Initialize Skills
    weather_skill = WeatherLookupSkill()
    crop_skill = CropAnalysisSkill()
    finance_skill = FinanceCalcSkill()
    
    # 3. Initialize Agents with shared Memory and Skills
    weather_agent = WeatherAgent(memory=short_term_mem, skills=[weather_skill])
    crop_agent = CropAgent(memory=short_term_mem, skills=[crop_skill])
    finance_agent = FinanceAgent(memory=short_term_mem, skills=[finance_skill])
    planner_agent = PlannerAgent(memory=short_term_mem, long_term_memory=long_term_mem)
    
    # --- SEQUENCE EXECUTION ---
    
    # Step 1: Weather Agent
    print(f"\n[1] Activating {weather_agent.name}...")
    w_res = await weather_agent.run(input_text=location)
    print(f"    -> Analysis: {w_res['analysis']}")
    print(f"    -> Restriction: {w_res['action_restriction']}")
    
    # Step 2: Crop Agent
    print(f"\n[2] Activating {crop_agent.name}...")
    c_res = await crop_agent.run(
        input_text="", 
        context={"crop_type": crop_type, "farm_size_acres": farm_size_acres}
    )
    print(f"    -> Recommendation: {c_res['fertilizer_recommendation']}")
    print(f"    -> Daily Water Required: {c_res['daily_water_required_liters']:,} liters")
    
    # Step 3: Finance Agent
    print(f"\n[3] Activating {finance_agent.name}...")
    f_res = await finance_agent.run(
        input_text="",
        context={"crop_type": crop_type, "farm_size_acres": farm_size_acres}
    )
    print(f"    -> {f_res['budget_verdict']}")
    
    # Step 4: Planner Agent
    print(f"\n[4] Activating {planner_agent.name} (Orchestrator)...")
    plan_res = await planner_agent.run(input_text="Generate plan")
    
    # Print results
    print(f"\n------------------------------------------")
    print(f" FINAL SYNTHESIZED 7-DAY ACTION PLAN")
    print(f"------------------------------------------")
    if plan_res["warnings_applied"]:
        for warning in plan_res["warnings_applied"]:
            print(f"[WARNING] {warning}")
            
    print(f"Financial Summary:")
    print(f"  - Est. Cost: {plan_res['financial_summary']['estimated_operating_cost']}")
    print(f"  - Proj. Profit: {plan_res['financial_summary']['projected_profit']}")
    print(f"Weather: {plan_res['weather_snapshot']}")
    
    print("\nSchedule:")
    for day_plan in plan_res["seven_day_plan"]:
        tasks_str = ", ".join(day_plan["tasks"])
        print(f"  {day_plan['day']:<10}: {tasks_str}")

async def main():
    print("Initializing Long-Term Memory (Prepopulating Agricultural Guidelines)...")
    long_term_mem = LongTermMemory()
    
    # Scenario 1: California (expected dry weather, corn)
    await run_scenario(
        scenario_id=1,
        location="California",
        crop_type="corn",
        farm_size_acres=15.0,
        long_term_mem=long_term_mem
    )
    
    # Scenario 2: Iowa (expected rainy weather, soybeans - should trigger fertilizer runoff caution from long term memory)
    await run_scenario(
        scenario_id=2,
        location="Iowa",
        crop_type="soybeans",
        farm_size_acres=50.0,
        long_term_mem=long_term_mem
    )

if __name__ == "__main__":
    asyncio.run(main())
