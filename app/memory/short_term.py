from typing import Any, Dict, List
from app.memory.base import BaseMemory

class ShortTermMemory(BaseMemory):
    """
    Manages transient session-based conversational memory for agents.
    Provides structured dictionary storage for quick blackboard-style reads.
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def add(self, data: Dict[str, Any]) -> None:
        """
        Add data to memory. Data should be a dict containing a 'key' and its 'value'.
        """
        self.history.append(data)

    def retrieve(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve elements. Filters elements where query matches the sender or the keys.
        """
        q = query.lower().strip()
        results = []
        for item in self.history:
            # Check if query matches keys or content in the stored dict
            match_found = False
            for k, v in item.items():
                if q in str(k).lower() or q in str(v).lower():
                    match_found = True
                    break
            if match_found:
                results.append(item)
                
        return results[-limit:]

    def clear(self) -> None:
        self.history.clear()
        
    def get_all(self) -> List[Dict[str, Any]]:
        return self.history
