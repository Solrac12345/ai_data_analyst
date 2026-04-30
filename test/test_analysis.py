# EN: Unit tests for AnalysisAgent
# FR: Tests unitaires pour AnalysisAgent

import pandas as pd
from typing import Any
from src.core.state import AnalysisState
from src.agents.analysis import AnalysisAgent


def test_analysis_success() -> None:
    """Test successful analysis with numeric data."""
    df = pd.DataFrame(
        {"A": [1, 2, 3, 4, 5], "B": [2, 4, 6, 8, 10], "C": ["x", "y", "x", "y", "x"]}
    )
    state = AnalysisState(clean_data=df)
    agent = AnalysisAgent()
    result = agent.execute(state)

    assert result.summary_stats is not None
    assert "A" in result.summary_stats
    assert result.correlations is not None
    assert "A" in result.correlations
    assert len(result.insights) > 0


def test_analysis_missing_data() -> None:
    """Test error handling when clean_data is missing."""
    state = AnalysisState(clean_data=None)
    agent = AnalysisAgent()
    result = agent.execute(state)

    assert not result.is_valid()
    assert any("No clean_data" in err for err in result.errors)
    assert result.summary_stats is None


def test_correlation_values() -> None:
    """Test that correlation matrix calculates correctly."""
    df = pd.DataFrame({"X": [1, 2, 3], "Y": [1, 2, 3]})
    state = AnalysisState(clean_data=df)
    agent = AnalysisAgent()
    result = agent.execute(state)

    assert result.correlations is not None
    # Perfect correlation should be 1.0
    assert result.correlations["X"]["Y"] == 1.0
    assert result.correlations["Y"]["X"] == 1.0


def test_insights_generation(monkeypatch: Any) -> None:
    """Test that insights are generated and truncated correctly."""
    df = pd.DataFrame({"A": range(100), "B": range(100)})
    state = AnalysisState(clean_data=df)
    # Override insight limit for testing
    monkeypatch.setattr("src.agents.analysis.settings.analysis.top_insights", 2)

    agent = AnalysisAgent()
    result = agent.execute(state)

    assert len(result.insights) <= 2
    assert any("Dataset contains" in insight for insight in result.insights)
