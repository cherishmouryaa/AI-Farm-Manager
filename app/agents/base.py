from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.memory.base import BaseMemory
from app.skills.base import BaseSkill

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the AI Farm Manager.
    """
    def __init__(
        self,
        name: str,
        role: str,
        memory: BaseMemory | None = None,
        skills: List[BaseSkill] | None = None
    ):
        self.name = name
        self.role = role
        self.memory = memory
        self.skills = skills or []

    @abstractmethod
    async def run(self, input_text: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Execute the agent's primary decision making logic.
        """
        pass

    def add_skill(self, skill: BaseSkill) -> None:
        """
        Dynamically add a skill to the agent's toolkit.
        """
        self.skills.append(skill)
