from typing import Any, Dict, List
from app.agents.base import BaseAgent
from app.memory.long_term import LongTermMemory

class PlannerAgent(BaseAgent):
    """
    Agent responsible for synthesizing inputs from all other agents and memory
    to design a cohesive 7-day action plan for the farmer.
    """
    def __init__(self, long_term_memory: LongTermMemory | None = None, **kwargs):
        super().__init__(
            name="Planner Agent",
            role="Coordinates multi-agent tasks and designs weekly farming plans.",
            **kwargs
        )
        self.long_term_memory = long_term_memory

    async def run(self, input_text: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        weather_analysis = "No weather context available."
        action_restriction = "none"
        rain_probability = 0
        fertilizer_recommendation = "Standard compost."
        total_costs = 0.0
        projected_profit = 0.0
        
        # 1. Retrieve data from shared Short-Term Memory
        if self.memory:
            weather_reports = self.memory.retrieve("weather_report", limit=1)
            if weather_reports:
                w_data = weather_reports[0]["data"]
                weather_analysis = w_data["analysis"]
                action_restriction = w_data["action_restriction"]
                rain_probability = w_data["weather_data"]["rain_probability"]
                
            crop_reports = self.memory.retrieve("crop_report", limit=1)
            if crop_reports:
                c_data = crop_reports[0]["data"]
                fertilizer_recommendation = c_data["fertilizer_recommendation"]
                
            finance_reports = self.memory.retrieve("finance_report", limit=1)
            if finance_reports:
                f_data = finance_reports[0]["data"]
                total_costs = f_data["financials"]["total_estimated_cost"]
                projected_profit = f_data["financials"]["net_profit"]
        
        # 2. Query Long-Term Memory for agricultural domain rules
        warnings_applied = []
        if self.long_term_memory:
            # Query about fertilizer delays
            fertilizer_rules = self.long_term_memory.retrieve("fertilizer delay")
            if fertilizer_rules and rain_probability > 70:
                warnings_applied.append(f"RULE COMPLIANCE: {fertilizer_rules[0]['rule']}")
                fertilizer_recommendation = f"POSTPONED (Due to high rain probability of {rain_probability}%)"

        # 3. Synthesize 7-Day Plan
        schedule = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for i, day in enumerate(days):
            tasks = []
            if i == 0:
                tasks.append("Calibrate soil moisture sensors.")
            
            # Irrigation planning
            if "increase irrigation" in action_restriction:
                tasks.append("Perform double irrigation cycle due to extreme heat forecast.")
            elif action_restriction == "delay spraying and harvesting" and i < 2:
                tasks.append("Irrigation suspended (Heavy rain expected).")
            else:
                tasks.append("Execute normal irrigation cycle.")
                
            # Fertilization planning
            if i == 1:
                tasks.append(f"Apply Fertilizer: {fertilizer_recommendation}")
                
            # General maintenance
            if i == 3:
                tasks.append("Conduct visual pest monitoring target scan.")
            if i == 5:
                tasks.append("Review weekly equipment states.")
                
            schedule.append({
                "day": day,
                "tasks": tasks
            })
            
        result = {
            "agent": self.name,
            "status": "success",
            "warnings_applied": warnings_applied,
            "financial_summary": {
                "estimated_operating_cost": f"${total_costs:,.2f}",
                "projected_profit": f"${projected_profit:,.2f}"
            },
            "weather_snapshot": weather_analysis,
            "seven_day_plan": schedule
        }
        
        if self.memory:
            self.memory.add({"sender": self.name, "topic": "final_plan", "data": result})
            
        return result
