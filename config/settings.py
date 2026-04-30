# Loads and validates application settings from YAML and environment variables

from pathlib import Path
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataConfig(BaseSettings):
    """Configuration for data loading."""
    default_path: Path = Field(default=Path("data/sample_dirty.csv"))
    encoding: str = Field(default="utf-8")


class CleaningConfig(BaseSettings):
    """Configuration for data cleaning parameters."""
    drop_duplicates: bool = True
    fill_missing: Literal["mean", "median", "drop"] = "mean"
    outlier_threshold: float = Field(ge=1.0, le=10.0, default=3.0)


class AnalysisConfig(BaseSettings):
    """Configuration for data analysis parameters."""
    correlation_method: Literal["pearson", "spearman", "kendall"] = "pearson"
    top_insights: int = Field(ge=1, le=20, default=5)


class VizConfig(BaseSettings):
    """Configuration for visualization parameters."""
    library: Literal["matplotlib", "plotly"] = "matplotlib"
    style: str = "default"


class Settings(BaseSettings):
    """Main application settings container."""
    model_config = SettingsConfigDict(
        yaml_file=Path(__file__).parent / "settings.yaml",
        env_file=".env",
        env_prefix="APP_",
        env_nested_delimiter="__",
        extra="ignore"
    )

    # EN: Nested config fields with type annotations
    data: DataConfig = Field(default_factory=DataConfig)
    cleaning: CleaningConfig = Field(default_factory=CleaningConfig)
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    visualization: VizConfig = Field(default_factory=VizConfig)


# Global singleton instance for easy import across the project
settings = Settings()