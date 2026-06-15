from typing import Any, Dict
from app.agents.base import BaseAgent
from app.skills.crop_analysis import CropAnalysisSkill

class CropAgent(BaseAgent):
    """
    Agent responsible for diagnosing crop requirements and calculating resources.
    """
    def __init__(self, **kwargs):
        super().__init__(
            name="Crop Agent",
            role="Diagnoses crop health issues and suggests growth optimizations.",
            **kwargs
        )

    async def run(self, input_text: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        # Extract variables
        crop_type = context.get("crop_type", "corn") if context else "corn"
        farm_size = context.get("farm_size_acres", 10.0) if context else 10.0
        
        # Find CropAnalysisSkill
        crop_tool = next((s for s in self.skills if isinstance(s, CropAnalysisSkill)), None)
        if not crop_tool:
            crop_tool = CropAnalysisSkill()  # Fallback
            
        crop_analysis = await crop_tool.run(crop_type=crop_type, farm_size_acres=farm_size)
        
        result = {
            "agent": self.name,
            "status": "success",
            "crop_analysis": crop_analysis,
            "fertilizer_recommendation": crop_analysis["fertilizer_recommendation"],
            "daily_water_required_liters": crop_analysis["daily_water_required_liters"]
        }
        
        # Write to memory if available
        if self.memory:
            self.memory.add({"sender": self.name, "topic": "crop_report", "data": result})
            
        return result
