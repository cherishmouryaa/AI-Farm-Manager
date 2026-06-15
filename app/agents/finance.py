from typing import Any, Dict
from app.agents.base import BaseAgent
from app.skills.finance_calc import FinanceCalcSkill

class FinanceAgent(BaseAgent):
    """
    Agent responsible for modeling agricultural ROI, cost tracking, and budgeting.
    """
    def __init__(self, **kwargs):
        super().__init__(
            name="Finance Agent",
            role="Handles financial planning, budget analysis, and agricultural investments ROI.",
            **kwargs
        )

    async def run(self, input_text: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        # Extract variables
        crop_type = context.get("crop_type", "corn") if context else "corn"
        farm_size = context.get("farm_size_acres", 10.0) if context else 10.0
        
        # Read daily water requirement from memory if available
        water_required = 10000.0  # Default fallback
        if self.memory:
            crop_reports = self.memory.retrieve("crop_report", limit=1)
            if crop_reports:
                water_required = crop_reports[0]["data"]["daily_water_required_liters"]
        
        # Find FinanceCalcSkill
        finance_tool = next((s for s in self.skills if isinstance(s, FinanceCalcSkill)), None)
        if not finance_tool:
            finance_tool = FinanceCalcSkill()
            
        financials = await finance_tool.run(
            crop_type=crop_type, 
            farm_size_acres=farm_size, 
            water_liters=water_required
        )
        
        result = {
            "agent": self.name,
            "status": "success",
            "financials": financials,
            "budget_verdict": f"Projected net profit for {farm_size} acres of {crop_type} is ${financials['net_profit']:.2f} (ROI: {financials['roi_percentage']}%)."
        }
        
        if self.memory:
            self.memory.add({"sender": self.name, "topic": "finance_report", "data": result})
            
        return result
