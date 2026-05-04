# EN: Pydantic models for API request/response validation
# FR: Modèles Pydantic pour la validation des requêtes/réponses API

from pydantic import BaseModel, Field
from typing import Optional


class AnalyzeRequest(BaseModel):
    """Request payload for triggering analysis."""

    data_path: str = Field(..., description="Path to the CSV or Excel file")
    output_dir: str = Field(default="output", description="Directory for plots/logs")
    report_path: str = Field(
        default="output/report.html", description="Path for the HTML report"
    )


class AnalyzeResponse(BaseModel):
    """Response payload after analysis completes."""

    status: str = Field(..., description="success or error")
    message: Optional[str] = Field(default=None, description="Optional status message")
    report_url: Optional[str] = Field(
        default=None, description="Path to the generated report"
    )
    insights: list[str] = Field(default_factory=list, description="Generated insights")
    errors: list[str] = Field(
        default_factory=list, description="Pipeline errors if any"
    )
