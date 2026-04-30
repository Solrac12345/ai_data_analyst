# Abstract base class for all agents in the pipeline

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from src.core.state import AnalysisState

S = TypeVar("S", bound=AnalysisState)


class BaseAgent(ABC, Generic[S]):
    """Abstract base class for all pipeline agents."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def execute(self, state: S) -> S:
        """Process the state and return the modified state."""
        pass

    def log(self, message: str, level: str = "INFO") -> None:
        """Simple logging helper for agent execution traces."""
        print(f"[{self.name}:{level}] {message}")
