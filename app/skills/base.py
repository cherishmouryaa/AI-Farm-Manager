from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseSkill(ABC):
    """
    Abstract base class for tools/skills that agents can execute.
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def run(self, **kwargs) -> Any:
        """
        Execute the tool action.
        """
        pass
