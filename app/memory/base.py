from abc import ABC, abstractmethod
from typing import Any, List

class BaseMemory(ABC):
    """
    Abstract base class for all memory management in the AI Farm Manager.
    """
    @abstractmethod
    def add(self, data: Any) -> None:
        """
        Add new information to memory.
        """
        pass

    @abstractmethod
    def retrieve(self, query: str, limit: int = 5) -> List[Any]:
        """
        Retrieve relevant information based on query.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clear memory content.
        """
        pass
