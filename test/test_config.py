# test/test_config.py
# Tests for configuration loading, validation, and environment variable overrides

import pytest
from pydantic import ValidationError
from config.settings import Settings, CleaningConfig


def test_defaults_match_yaml():
    """Verify that default values match the YAML configuration."""
    s = Settings()
    assert s.cleaning.outlier_threshold == 3.0
    assert s.visualization.library == "matplotlib"
    assert s.analysis.correlation_method == "pearson"


def test_env_override(monkeypatch):
    """Test that environment variables correctly override YAML defaults."""
    # Use double underscore for nested fields: APP_DATA__DEFAULT_PATH
    monkeypatch.setenv("APP_DATA__DEFAULT_PATH", "data/test_override.csv")
    s = Settings()
    assert s.data.default_path.name == "test_override.csv"


def test_invalid_strategy_raises() -> None:
    """Ensure invalid cleaning strategies raise a validation error."""
    with pytest.raises(ValidationError):
        # EN: Ignore mypy error because we intentionally pass an invalid literal
        CleaningConfig(fill_missing="magic")  # type: ignore[arg-type]


def test_threshold_bounds():
    """Verify outlier threshold enforces valid bounds (1.0 to 10.0)."""
    with pytest.raises(ValidationError):
        CleaningConfig(outlier_threshold=0.5)
    with pytest.raises(ValidationError):
        CleaningConfig(outlier_threshold=12.0)
