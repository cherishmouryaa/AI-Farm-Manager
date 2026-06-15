from typing import Any, Dict
from app.skills.base import BaseSkill

class FinanceCalcSkill(BaseSkill):
    """
    Skill for running farm cost models, ROI estimates, and profit margins.
    """
    def __init__(self):
        super().__init__(
            name="Finance Calculator",
            description="Calculates operational budgets, revenue projections, and expected ROI."
        )

    async def run(self, crop_type: str, farm_size_acres: float, water_liters: float, **kwargs) -> Dict[str, Any]:
        # Simple cost constants for calculation
        base_labor_cost_per_acre = 100.0  # USD
        base_seed_cost_per_acre = 50.0   # USD
        water_cost_per_liter = 0.005      # USD (e.g. municipal/pumping cost)
        
        # Crop yield estimates (tons per acre) and price per ton
        crop_market_rates = {
            "corn": {"yield_per_acre": 4.5, "price_per_ton": 180.0},
            "wheat": {"yield_per_acre": 2.5, "price_per_ton": 220.0},
            "soybeans": {"yield_per_acre": 1.5, "price_per_ton": 380.0}
        }
        
        rate_info = crop_market_rates.get(crop_type.lower().strip(), {"yield_per_acre": 3.0, "price_per_ton": 200.0})
        
        # Calculations
        seed_cost = base_seed_cost_per_acre * farm_size_acres
        labor_cost = base_labor_cost_per_acre * farm_size_acres
        water_cost = water_liters * water_cost_per_liter
        fertilizer_cost = 80.0 * farm_size_acres  # Mock $80/acre fertilizer cost
        
        total_estimated_cost = seed_cost + labor_cost + water_cost + fertilizer_cost
        
        projected_yield_tons = rate_info["yield_per_acre"] * farm_size_acres
        projected_revenue = projected_yield_tons * rate_info["price_per_ton"]
        
        net_profit = projected_revenue - total_estimated_cost
        roi = (net_profit / total_estimated_cost) * 100 if total_estimated_cost > 0 else 0.0

        return {
            "farm_size_acres": farm_size_acres,
            "cost_breakdown": {
                "seeds": seed_cost,
                "labor": labor_cost,
                "water": water_cost,
                "fertilizer": fertilizer_cost
            },
            "total_estimated_cost": total_estimated_cost,
            "projected_yield_tons": projected_yield_tons,
            "projected_revenue": projected_revenue,
            "net_profit": net_profit,
            "roi_percentage": round(roi, 2)
        }
