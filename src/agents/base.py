# Abstract base class for all agents in the pipeline

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from src.core.state import AnalysisState

# Type variable for state inheritance
S = TypeVar("S", bound=AnalysisState)


class BaseAgent(ABC, Generic[S]):
    """
    Abstract base class for all pipeline agents.
    Enforces consistent interface: execute(state) -> state
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, state: S) -> S:
        """
        Process the state and return the modified state.
        Must be implemented by each concrete agent.
        """
        pass

    def log(self, message: str, level: str = "INFO") -> None:
        """Simple logging helper for agent execution traces."""
        print(f"[{self.name}:{level}] {message}")
