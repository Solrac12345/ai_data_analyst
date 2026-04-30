# Defines the Pydantic state object passed through the LangGraph workflow

from typing import Any, Optional
from pydantic import BaseModel, Field


class AnalysisState(BaseModel):
    """Shared state container for the multi-agent data analysis pipeline."""

    # Data loading stage
    raw_data: Optional[Any] = Field(default=None, description="Raw DataFrame")
    data_path: Optional[str] = Field(default=None, description="Path to dataset")

    # Cleaning stage
    clean_data: Optional[Any] = Field(default=None, description="Cleaned DataFrame")
    cleaning_report: dict[str, Any] = Field(
        default_factory=dict, description="Cleaning summary"
    )

    # Analysis stage
    summary_stats: Optional[dict[str, Any]] = Field(default=None, description="Stats")
    correlations: Optional[dict[str, Any]] = Field(
        default=None, description="Correlations"
    )
    insights: list[str] = Field(default_factory=list, description="Insights")

    # Visualization stage
    plots_code: list[str] = Field(default_factory=list, description="Plot code")
    plot_paths: list[str] = Field(default_factory=list, description="Plot paths")

    # Pipeline control
    current_step: str = Field(default="load", description="Current step")
    errors: list[str] = Field(default_factory=list, description="Errors")

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def is_valid(self) -> bool:
        return len(self.errors) == 0
