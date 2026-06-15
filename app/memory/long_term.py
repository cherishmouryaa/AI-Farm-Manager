from typing import Any, List
from app.memory.base import BaseMemory

class LongTermMemory(BaseMemory):
    """
    Manages persistent semantic memory, acting as a knowledge repository for agents.
    Allows pre-populating with agricultural knowledge databases.
    """
    def __init__(self):
        self.kb: List[Any] = []
        # Prepopulate with some offline agricultural knowledge bases (useful for offline Kaggle context)
        self.prepopulate_kb()

    def prepopulate_kb(self) -> None:
        self.kb.append({
            "topic": "fertilizer delay",
            "rule": "Always delay nitrogen application if rain probability is above 70% to prevent nutrient runoff."
        })
        self.kb.append({
            "topic": "frost warning",
            "rule": "If temperatures drop below 2°C, trigger overnight irrigation (mist/sprinkler) to protect buds."
        })
        self.kb.append({
            "topic": "water conservation",
            "rule": "Reduce irrigation by 50% on days immediately following rain of > 10mm."
        })

    def add(self, data: Any) -> None:
        self.kb.append(data)

    def retrieve(self, query: str, limit: int = 5) -> List[Any]:
        # Simple substring match to mimic semantic search
        q = query.lower().strip()
        results = []
        for item in self.kb:
            if isinstance(item, dict):
                # Search across all values in the dictionary
                if any(q in str(val).lower() for val in item.values()):
                    results.append(item)
            elif q in str(item).lower():
                results.append(item)
        return results[:limit]

    def clear(self) -> None:
        self.kb.clear()
