# test/test_viz.py
# EN: Unit tests for VizAgent
# FR: Tests unitaires pour VizAgent

import pandas as pd
from typing import Any
from src.core.state import AnalysisState
from src.agents.viz import VizAgent


def test_viz_matplotlib(monkeypatch: Any) -> None:
    """Test code generation for Matplotlib."""
    df = pd.DataFrame({"A": [1, 2, 2, 3, 3, 3]})
    state = AnalysisState(clean_data=df)

    # Force matplotlib setting
    monkeypatch.setattr("src.agents.viz.settings.visualization.library", "matplotlib")

    agent = VizAgent()
    result = agent.execute(state)

    assert len(result.plots_code) == 1
    assert "plt.hist" in result.plots_code[0]
    assert result.plot_paths[0].endswith(".png")


def test_viz_plotly(monkeypatch: Any) -> None:
    """Test code generation for Plotly."""
    df = pd.DataFrame({"B": [10, 20, 30]})
    state = AnalysisState(clean_data=df)

    # Force plotly setting
    monkeypatch.setattr("src.agents.viz.settings.visualization.library", "plotly")

    agent = VizAgent()
    result = agent.execute(state)

    assert len(result.plots_code) == 1
    assert "px.histogram" in result.plots_code[0]
    assert result.plot_paths[0].endswith(".html")


def test_viz_missing_data() -> None:
    """Test error handling when clean_data is missing."""
    state = AnalysisState(clean_data=None)
    agent = VizAgent()
    result = agent.execute(state)

    assert not result.is_valid()
    assert any("No clean_data" in err for err in result.errors)


def test_viz_no_numeric_columns() -> None:
    """Test behavior when no numeric columns are available."""
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "City": ["NY", "LA"]})
    state = AnalysisState(clean_data=df)

    agent = VizAgent()
    result = agent.execute(state)

    # Should be valid but no plots generated
    assert result.is_valid()
    assert len(result.plots_code) == 0
