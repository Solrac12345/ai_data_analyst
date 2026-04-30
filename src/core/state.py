# Defines the Pydantic state object passed through the LangGraph workflow

from typing import Any, Optional
from pydantic import BaseModel, Field


class AnalysisState(BaseModel):
    """
    Shared state container for the multi-agent data analysis pipeline.
    Each agent reads/writes only the fields relevant to its stage.
    """

    # Data loading stage
    raw_data: Optional[Any] = Field(
        default=None, description="Raw DataFrame from loader"
    )
    data_path: Optional[str] = Field(default=None, description="Path to loaded dataset")

    # Cleaning stage
    clean_data: Optional[Any] = Field(default=None, description="Cleaned DataFrame")
    cleaning_report: dict = Field(
        default_factory=dict, description="Summary of cleaning actions"
    )

    # Analysis stage
    summary_stats: Optional[dict] = Field(
        default=None, description="Descriptive statistics"
    )
    correlations: Optional[dict] = Field(default=None, description="Correlation matrix")
    insights: list[str] = Field(default_factory=list, description="Generated insights")

    # Visualization stage
    plots_code: list[str] = Field(
        default_factory=list, description="Generated plotting code"
    )
    plot_paths: list[str] = Field(
        default_factory=list, description="Paths to saved plots"
    )

    # Pipeline control
    current_step: str = Field(default="load", description="Current pipeline step")
    errors: list[str] = Field(default_factory=list, description="Accumulated errors")

    def add_error(self, message: str) -> None:
        """Append an error message to the state."""
        self.errors.append(message)

    def is_valid(self) -> bool:
        """Return True if no errors have been recorded."""
        return len(self.errors) == 0
